# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=invalid-overridden-method

import codecs
import sys
import warnings
from io import BytesIO, StringIO
from itertools import islice
from typing import AsyncIterator, Generic, IO, Optional, overload, TypeVar, Union

import asyncio

from azure.core.exceptions import HttpResponseError

from .._shared.request_handlers import validate_and_format_range_headers
from .._shared.response_handlers import process_storage_error, parse_length_from_content_range
from .._deserialize import deserialize_blob_properties, get_page_ranges_result
from .._download import process_range_and_offset, _ChunkDownloader
from .._encryption import (
    adjust_blob_size_for_encryption,
    decrypt_blob,
    is_encryption_v2,
    parse_encryption_data
)

T = TypeVar('T', bytes, str)


async def process_content(data, start_offset, end_offset, encryption):
    if data is None:
        raise ValueError("Response cannot be None.")
    content = data.response.body()
    if encryption.get('key') is not None or encryption.get('resolver') is not None:
        try:
            return decrypt_blob(
                encryption.get('required'),
                encryption.get('key'),
                encryption.get('resolver'),
                content,
                start_offset,
                end_offset,
                data.response.headers)
        except Exception as error:
            raise HttpResponseError(
                message="Decryption failed.",
                response=data.response,
                error=error) from error
    return content


class _AsyncChunkDownloader(_ChunkDownloader):
    def __init__(self, **kwargs):
        super(_AsyncChunkDownloader, self).__init__(**kwargs)
        self.stream_lock = asyncio.Lock() if kwargs.get('parallel') else None
        self.progress_lock = asyncio.Lock() if kwargs.get('parallel') else None

    async def process_chunk(self, chunk_start):
        chunk_start, chunk_end = self._calculate_range(chunk_start)
        chunk_data, _ = await self._download_chunk(chunk_start, chunk_end - 1)
        length = chunk_end - chunk_start
        if length > 0:
            await self._write_to_stream(chunk_data, chunk_start)
            await self._update_progress(length)

    async def yield_chunk(self, chunk_start):
        chunk_start, chunk_end = self._calculate_range(chunk_start)
        return await self._download_chunk(chunk_start, chunk_end - 1)

    async def _update_progress(self, length):
        if self.progress_lock:
            async with self.progress_lock:  # pylint: disable=not-async-context-manager
                self.progress_total += length
        else:
            self.progress_total += length

        if self.progress_hook:
            await self.progress_hook(self.progress_total, self.total_size)

    async def _write_to_stream(self, chunk_data, chunk_start):
        if self.stream_lock:
            async with self.stream_lock:  # pylint: disable=not-async-context-manager
                self.stream.seek(self.stream_start + (chunk_start - self.start_index))
                self.stream.write(chunk_data)
        else:
            self.stream.write(chunk_data)

    async def _download_chunk(self, chunk_start, chunk_end):
        download_range, offset = process_range_and_offset(
            chunk_start, chunk_end, chunk_end, self.encryption_options, self.encryption_data
        )

        # No need to download the empty chunk from server if there's no data in the chunk to be downloaded.
        # Do optimize and create empty chunk locally if condition is met.
        if self._do_optimize(download_range[0], download_range[1]):
            content_length = download_range[1] - download_range[0] + 1
            chunk_data = b"\x00" * content_length
        else:
            range_header, range_validation = validate_and_format_range_headers(
                download_range[0],
                download_range[1],
                check_content_md5=self.validate_content
            )
            try:
                _, response = await self.client.download(
                    range=range_header,
                    range_get_content_md5=range_validation,
                    validate_content=self.validate_content,
                    data_stream_total=self.total_size,
                    download_stream_current=self.progress_total,
                    **self.request_options
                )

            except HttpResponseError as error:
                process_storage_error(error)

            chunk_data = await process_content(response, offset[0], offset[1], self.encryption_options)
            content_length = response.content_length

            # This makes sure that if_match is set so that we can validate
            # that subsequent downloads are to an unmodified blob
            if self.request_options.get('modified_access_conditions'):
                self.request_options['modified_access_conditions'].if_match = response.properties.etag

        return chunk_data, content_length


class _AsyncChunkIterator(object):
    """Async iterator for chunks in blob download stream."""

    def __init__(self, size, content, downloader, chunk_size):
        self.size = size
        self._chunk_size = chunk_size
        self._current_content = content
        self._iter_downloader = downloader
        self._iter_chunks = None
        self._complete = size == 0

    def __len__(self):
        return self.size

    def __iter__(self):
        raise TypeError("Async stream must be iterated asynchronously.")

    def __aiter__(self):
        return self

    # Iterate through responses.
    async def __anext__(self):
        if self._complete:
            raise StopAsyncIteration("Download complete")
        if not self._iter_downloader:
            # cut the data obtained from initial GET into chunks
            if len(self._current_content) > self._chunk_size:
                return self._get_chunk_data()
            self._complete = True
            return self._current_content

        if not self._iter_chunks:
            self._iter_chunks = self._iter_downloader.get_chunk_offsets()

        # initial GET result still has more than _chunk_size bytes of data
        if len(self._current_content) >= self._chunk_size:
            return self._get_chunk_data()

        try:
            chunk = next(self._iter_chunks)
            self._current_content += (await self._iter_downloader.yield_chunk(chunk))[0]
        except StopIteration as exc:
            self._complete = True
            # it's likely that there some data left in self._current_content
            if self._current_content:
                return self._current_content
            raise StopAsyncIteration("Download complete") from exc

        return self._get_chunk_data()

    def _get_chunk_data(self):
        chunk_data = self._current_content[: self._chunk_size]
        self._current_content = self._current_content[self._chunk_size:]
        return chunk_data


class StorageStreamDownloader(Generic[T]):  # pylint: disable=too-many-instance-attributes
    """A streaming object to download from Azure Storage.

    :ivar str name:
        The name of the blob being downloaded.
    :ivar str container:
        The name of the container where the blob is.
    :ivar ~azure.storage.blob.BlobProperties properties:
        The properties of the blob being downloaded. If only a range of the data is being
        downloaded, this will be reflected in the properties.
    :ivar int size:
        The size of the total data in the stream. This will be the byte range if specified,
        otherwise the total size of the blob.
    """

    def __init__(
        self,
        clients=None,
        config=None,
        start_range=None,
        end_range=None,
        validate_content=None,
        encryption_options=None,
        max_concurrency=1,
        name=None,
        container=None,
        encoding=None,
        download_cls=None,
        **kwargs
    ):
        self.name = name
        self.container = container
        self.properties = None
        self.size = None

        self._clients = clients
        self._config = config
        self._start_range = start_range
        self._end_range = end_range
        self._max_concurrency = max_concurrency
        self._encoding = encoding
        self._validate_content = validate_content
        self._encryption_options = encryption_options or {}
        self._progress_hook = kwargs.pop('progress_hook', None)
        self._request_options = kwargs
        self._response = None
        self._location_mode = None
        self._current_content = b''
        self._file_size = 0
        self._non_empty_ranges = None
        self._encryption_data = None

        # The content download offset, after any processing (decryption), in bytes
        self._download_offset = 0
        # The raw download offset, before processing (decryption), in bytes
        self._raw_download_offset = 0
        # The offset the stream has been read to in bytes or chars depending on mode
        self._read_offset = 0
        # The offset into current_content that has been consumed in bytes or chars depending on mode
        self._current_content_offset = 0

        self._text_mode: Optional[bool] = None
        self._decoder = None
        # Whether the current content is the first chunk of download content or not
        self._first_chunk = True
        self._download_start = self._start_range or 0

        # The cls is passed in via download_cls to avoid conflicting arg name with Generic.__new__
        # but needs to be changed to cls in the request options.
        self._request_options['cls'] = download_cls

    def __len__(self):
        return self.size

    async def _get_encryption_data_request(self):
        # Save current request cls
        download_cls = self._request_options.pop('cls', None)
        # Adjust cls for get_properties
        self._request_options['cls'] = deserialize_blob_properties

        properties = await self._clients.blob.get_properties(**self._request_options)
        # This will return None if there is no encryption metadata or there are parsing errors.
        # That is acceptable here, the proper error will be caught and surfaced when attempting
        # to decrypt the blob.
        self._encryption_data = parse_encryption_data(properties.metadata)

        # Restore cls for download
        self._request_options['cls'] = download_cls

    async def _setup(self):
        if self._encryption_options.get("key") is not None or self._encryption_options.get("resolver") is not None:
            await self._get_encryption_data_request()

        # The service only provides transactional MD5s for chunks under 4MB.
        # If validate_content is on, get only self.MAX_CHUNK_GET_SIZE for the first
        # chunk so a transactional MD5 can be retrieved.
        first_get_size = (
            self._config.max_single_get_size if not self._validate_content else self._config.max_chunk_get_size
        )
        initial_request_start = self._start_range if self._start_range is not None else 0
        if self._end_range is not None and self._end_range - initial_request_start < first_get_size:
            initial_request_end = self._end_range
        else:
            initial_request_end = initial_request_start + first_get_size - 1

        # pylint: disable-next=attribute-defined-outside-init
        self._initial_range, self._initial_offset = process_range_and_offset(
            initial_request_start,
            initial_request_end,
            self._end_range,
            self._encryption_options,
            self._encryption_data
        )

        self._response = await self._initial_request()

        self.properties = self._response.properties
        self.properties.name = self.name
        self.properties.container = self.container

        # Set the content length to the download size instead of the size of the last range
        self.properties.size = self.size
        self.properties.content_range = (f"bytes {self._download_start}-"
                                         f"{self._end_range if self._end_range is not None else self._file_size - 1}/"
                                         f"{self._file_size}")

        # Overwrite the content MD5 as it is the MD5 for the last range instead
        # of the stored MD5
        # TODO: Set to the stored MD5 when the service returns this
        self.properties.content_md5 = None

    @property
    def _download_complete(self):
        if is_encryption_v2(self._encryption_data):
            return self._download_offset >= self.size
        return self._raw_download_offset >= self.size

    async def _initial_request(self):
        range_header, range_validation = validate_and_format_range_headers(
            self._initial_range[0],
            self._initial_range[1],
            start_range_required=False,
            end_range_required=False,
            check_content_md5=self._validate_content)

        try:
            location_mode, response = await self._clients.blob.download(
                range=range_header,
                range_get_content_md5=range_validation,
                validate_content=self._validate_content,
                data_stream_total=None,
                download_stream_current=0,
                **self._request_options)

            # Check the location we read from to ensure we use the same one
            # for subsequent requests.
            self._location_mode = location_mode

            # Parse the total file size and adjust the download size if ranges
            # were specified
            self._file_size = parse_length_from_content_range(response.properties.content_range)
            if self._file_size is None:
                raise ValueError("Required Content-Range response header is missing or malformed.")
            # Remove any extra encryption data size from blob size
            self._file_size = adjust_blob_size_for_encryption(self._file_size, self._encryption_data)

            if self._end_range is not None:
                # Use the length unless it is over the end of the file
                self.size = min(self._file_size - self._start_range, self._end_range - self._start_range + 1)
            elif self._start_range is not None:
                self.size = self._file_size - self._start_range
            else:
                self.size = self._file_size

        except HttpResponseError as error:
            if self._start_range is None and error.response and error.status_code == 416:
                # Get range will fail on an empty file. If the user did not
                # request a range, do a regular get request in order to get
                # any properties.
                try:
                    _, response = await self._clients.blob.download(
                        validate_content=self._validate_content,
                        data_stream_total=0,
                        download_stream_current=0,
                        **self._request_options)
                except HttpResponseError as e:
                    process_storage_error(e)

                # Set the download size to empty
                self.size = 0
                self._file_size = 0
            else:
                process_storage_error(error)

        if self.size == 0:
            self._current_content = b""
        else:
            self._current_content = await process_content(
                response,
                self._initial_offset[0],
                self._initial_offset[1],
                self._encryption_options
            )
        self._download_offset += len(self._current_content)
        self._raw_download_offset += response.content_length

        # get page ranges to optimize downloading sparse page blob
        if response.properties.blob_type == 'PageBlob':
            try:
                page_ranges = await self._clients.page_blob.get_page_ranges()
                self._non_empty_ranges = get_page_ranges_result(page_ranges)[0]
            except HttpResponseError:
                pass

        if not self._download_complete and self._request_options.get("modified_access_conditions"):
            self._request_options["modified_access_conditions"].if_match = response.properties.etag

        return response

    def chunks(self):
        # type: () -> AsyncIterator[bytes]
        """
        Iterate over chunks in the download stream. Note, the iterator returned will
        iterate over the entire download content, regardless of any data that was
        previously read.

        NOTE: If the stream has been partially read, some data may be re-downloaded by the iterator.

        :returns: An async iterator of the chunks in the download stream.
        :rtype: AsyncIterator[bytes]

        .. admonition:: Example:

            .. literalinclude:: ../samples/blob_samples_hello_world_async.py
                :start-after: [START download_a_blob_in_chunk]
                :end-before: [END download_a_blob_in_chunk]
                :language: python
                :dedent: 16
                :caption: Download a blob using chunks().
        """
        if self._text_mode:
            raise ValueError("Stream has been partially read in text mode. chunks is not supported in text mode.")
        if self._encoding:
            warnings.warn("Encoding is ignored with chunks as only bytes are supported.")

        iter_downloader = None
        # If we still have the first chunk buffered, use it. Otherwise, download all content again
        if not self._first_chunk or not self._download_complete:
            if self._first_chunk:
                start = self._download_start + len(self._current_content)
                current_progress = len(self._current_content)
            else:
                start = self._download_start
                current_progress = 0

            end = self._download_start + self.size

            iter_downloader = _AsyncChunkDownloader(
                client=self._clients.blob,
                non_empty_ranges=self._non_empty_ranges,
                total_size=self.size,
                chunk_size=self._config.max_chunk_get_size,
                current_progress=current_progress,
                start_range=start,
                end_range=end,
                validate_content=self._validate_content,
                encryption_options=self._encryption_options,
                encryption_data=self._encryption_data,
                use_location=self._location_mode,
                **self._request_options
            )

        initial_content = self._current_content if self._first_chunk else b''
        return _AsyncChunkIterator(
            size=self.size,
            content=initial_content,
            downloader=iter_downloader,
            chunk_size=self._config.max_chunk_get_size)

    @overload
    def read(self, size: int = -1) -> T:
        ...

    @overload
    def read(self, *, chars: Optional[int] = None) -> T:
        ...

    # pylint: disable-next=too-many-statements,too-many-branches
    async def read(self, size: int = -1, *, chars: Optional[int] = None) -> T:
        """
        Read the specified bytes or chars from the stream. If `encoding`
        was specified on `download_blob`, it is recommended to use the
        chars parameter to read a specific number of chars to avoid decoding
        errors. If size/chars is unspecified or negative all bytes will be read.

        :param int size:
            The number of bytes to download from the stream. Leave unspecified
            or set negative to download all bytes.
        :keyword Optional[int] chars:
            The number of chars to download from the stream. Leave unspecified
            or set negative to download all chars. Note, this can only be used
            when encoding is specified on `download_blob`.
        :returns:
            The requested data as bytes or a string if encoding was specified. If
            the return value is empty, there is no more data to read.
        :rtype: T
        """
        if size > -1 and self._encoding:
            warnings.warn(
                "Size parameter specified with text encoding enabled. It is recommended to use chars "
                "to read a specific number of characters instead."
            )
        if size > -1 and chars is not None:
            raise ValueError("Cannot specify both size and chars.")
        if not self._encoding and chars is not None:
            raise ValueError("Must specify encoding to read chars.")
        if self._text_mode and size > -1:
            raise ValueError("Stream has been partially read in text mode. Please use chars.")
        if self._text_mode is False and chars is not None:
            raise ValueError("Stream has been partially read in bytes mode. Please use size.")

        # Empty blob or already read to the end
        if (size == 0 or chars == 0 or
                (self._download_complete and self._current_content_offset >= len(self._current_content))):
            return b'' if not self._encoding else ''

        if not self._text_mode and chars is not None:
            self._text_mode = True
            self._decoder = codecs.getincrementaldecoder(self._encoding)('strict')
            self._current_content = self._decoder.decode(self._current_content, final=self._download_complete)
        elif self._text_mode is None:
            self._text_mode = False

        output_stream: Union[BytesIO, StringIO]
        if self._text_mode:
            output_stream = StringIO()
            size = chars if chars else sys.maxsize
        else:
            output_stream = BytesIO()
            size = size if size > 0 else sys.maxsize
        readall = size == sys.maxsize
        count = 0

        # Start by reading from current_content
        start = self._current_content_offset
        length = min(len(self._current_content) - self._current_content_offset, size - count)
        read = output_stream.write(self._current_content[start:start + length])

        count += read
        self._current_content_offset += read
        self._read_offset += read
        await self._check_and_report_progress()

        remaining = size - count
        if remaining > 0 and not self._download_complete:
            # Create a downloader than can download the rest of the file
            start = self._download_start + self._download_offset
            end = self._download_start + self.size

            parallel = self._max_concurrency > 1
            downloader = _AsyncChunkDownloader(
                client=self._clients.blob,
                non_empty_ranges=self._non_empty_ranges,
                total_size=self.size,
                chunk_size=self._config.max_chunk_get_size,
                current_progress=self._read_offset,
                start_range=start,
                end_range=end,
                stream=output_stream,
                parallel=parallel,
                validate_content=self._validate_content,
                encryption_options=self._encryption_options,
                encryption_data=self._encryption_data,
                use_location=self._location_mode,
                progress_hook=self._progress_hook,
                **self._request_options
            )
            self._first_chunk = False

            # When reading all data, have the downloader read everything into the stream.
            # Else, read one chunk at a time (using the downloader as an iterator) until
            # the requested size is reached.
            chunks_iter = downloader.get_chunk_offsets()
            if readall and not self._text_mode:
                running_futures = [
                    asyncio.ensure_future(downloader.process_chunk(d))
                    for d in islice(chunks_iter, 0, self._max_concurrency)
                ]
                while running_futures:
                    # Wait for some download to finish before adding a new one
                    done, running_futures = await asyncio.wait(
                        running_futures, return_when=asyncio.FIRST_COMPLETED)
                    try:
                        for task in done:
                            task.result()
                    except HttpResponseError as error:
                        process_storage_error(error)
                    try:
                        for _ in range(0, len(done)):
                            next_chunk = next(chunks_iter)
                            running_futures.add(asyncio.ensure_future(downloader.process_chunk(next_chunk)))
                    except StopIteration:
                        break

                if running_futures:
                    # Wait for the remaining downloads to finish
                    done, _running_futures = await asyncio.wait(running_futures)
                    try:
                        for task in done:
                            task.result()
                    except HttpResponseError as error:
                        process_storage_error(error)

                self._complete_read()

            else:
                while (chunk := next(chunks_iter, None)) is not None and remaining > 0:
                    chunk_data, content_length = await downloader.yield_chunk(chunk)
                    self._download_offset += len(chunk_data)
                    self._raw_download_offset += content_length
                    self._current_content = self._decoder.decode(
                        chunk_data, final=self._download_complete) if self._text_mode else chunk_data

                    if remaining < len(self._current_content):
                        read = output_stream.write(self._current_content[:remaining])
                    else:
                        read = output_stream.write(self._current_content)

                    self._current_content_offset = read
                    self._read_offset += read
                    remaining -= read
                    await self._check_and_report_progress()

        data = output_stream.getvalue()
        if not self._text_mode and self._encoding:
            try:
                # This is technically incorrect to do, but we have it for backwards compatibility.
                data = data.decode(self._encoding)
            except UnicodeDecodeError:
                warnings.warn(
                    "Encountered a decoding error while decoding blob data from a partial read. "
                    "Try using the `chars` keyword instead to read in text mode."
                )
                raise

        return data

    async def readall(self) -> T:
        """
        Read the entire contents of this blob.
        This operation is blocking until all data is downloaded.

        :returns: The requested data as bytes or a string if encoding was specified.
        :rtype: T
        """
        return await self.read()

    async def readinto(self, stream: IO[bytes]) -> int:
        """Download the contents of this blob to a stream.

        :param IO[bytes] stream:
            The stream to download to. This can be an open file-handle,
            or any writable stream. The stream must be seekable if the download
            uses more than one parallel connection.
        :returns: The number of bytes read.
        :rtype: int
        """
        if self._text_mode:
            raise ValueError("Stream has been partially read in text mode. readinto is not supported in text mode.")
        if self._encoding:
            warnings.warn("Encoding is ignored with readinto as only byte streams are supported.")

        # the stream must be seekable if parallel download is required
        parallel = self._max_concurrency > 1
        if parallel:
            error_message = "Target stream handle must be seekable."
            if sys.version_info >= (3,) and not stream.seekable():
                raise ValueError(error_message)

            try:
                stream.seek(stream.tell())
            except (NotImplementedError, AttributeError) as exc:
                raise ValueError(error_message) from exc

        # If some data has been streamed using `read`, only stream the remaining data
        remaining_size = self.size - self._read_offset
        # Already read to the end
        if remaining_size <= 0:
            return 0

        # Write the current content to the user stream
        current_remaining = len(self._current_content) - self._current_content_offset
        start = self._current_content_offset
        count = stream.write(self._current_content[start:start + current_remaining])

        self._current_content_offset += count
        self._read_offset += count
        if self._progress_hook:
            await self._progress_hook(self._read_offset, self.size)

        # If all the data was already downloaded/buffered
        if self._download_complete:
            return remaining_size

        data_start = self._download_start + self._read_offset
        data_end = self._download_start + self.size

        downloader = _AsyncChunkDownloader(
            client=self._clients.blob,
            non_empty_ranges=self._non_empty_ranges,
            total_size=self.size,
            chunk_size=self._config.max_chunk_get_size,
            current_progress=self._read_offset,
            start_range=data_start,
            end_range=data_end,
            stream=stream,
            parallel=parallel,
            validate_content=self._validate_content,
            encryption_options=self._encryption_options,
            encryption_data=self._encryption_data,
            use_location=self._location_mode,
            progress_hook=self._progress_hook,
            **self._request_options
        )

        dl_tasks = downloader.get_chunk_offsets()
        running_futures = [
            asyncio.ensure_future(downloader.process_chunk(d))
            for d in islice(dl_tasks, 0, self._max_concurrency)
        ]
        while running_futures:
            # Wait for some download to finish before adding a new one
            done, running_futures = await asyncio.wait(
                running_futures, return_when=asyncio.FIRST_COMPLETED)
            try:
                for task in done:
                    task.result()
            except HttpResponseError as error:
                process_storage_error(error)
            try:
                for _ in range(0, len(done)):
                    next_chunk = next(dl_tasks)
                    running_futures.add(asyncio.ensure_future(downloader.process_chunk(next_chunk)))
            except StopIteration:
                break

        if running_futures:
            # Wait for the remaining downloads to finish
            done, _running_futures = await asyncio.wait(running_futures)
            try:
                for task in done:
                    task.result()
            except HttpResponseError as error:
                process_storage_error(error)

        self._complete_read()
        return remaining_size

    def _complete_read(self):
        """Adjusts all offsets to the end of the download."""
        self._download_offset = self.size
        self._raw_download_offset = self.size
        self._read_offset = self.size
        self._current_content_offset = len(self._current_content)

    async def _check_and_report_progress(self):
        """Reports progress if necessary."""
        # Only report progress at the end of each chunk and use download_offset to always report
        # progress in terms of (approximate) byte count.
        if self._progress_hook and self._current_content_offset == len(self._current_content):
            await self._progress_hook(self._download_offset, self.size)

    async def content_as_bytes(self, max_concurrency=1):
        """DEPRECATED: Download the contents of this file.

        This operation is blocking until all data is downloaded.

        This method is deprecated, use func:`readall` instead.

        :param int max_concurrency:
            The number of parallel connections with which to download.
        :returns: The contents of the file as bytes.
        :rtype: bytes
        """
        warnings.warn(
            "content_as_bytes is deprecated, use readall instead",
            DeprecationWarning
        )
        if self._text_mode:
            raise ValueError("Stream has been partially read in text mode. "
                             "content_as_bytes is not supported in text mode.")

        self._max_concurrency = max_concurrency
        return await self.readall()

    async def content_as_text(self, max_concurrency=1, encoding="UTF-8"):
        """DEPRECATED: Download the contents of this blob, and decode as text.

        This operation is blocking until all data is downloaded.

        This method is deprecated, use func:`readall` instead.

        :param int max_concurrency:
            The number of parallel connections with which to download.
        :param str encoding:
            Test encoding to decode the downloaded bytes. Default is UTF-8.
        :returns: The content of the file as a str.
        :rtype: str
        """
        warnings.warn(
            "content_as_text is deprecated, use readall instead",
            DeprecationWarning
        )
        if self._text_mode:
            raise ValueError("Stream has been partially read in text mode. "
                             "content_as_text is not supported in text mode.")

        self._max_concurrency = max_concurrency
        self._encoding = encoding
        return await self.readall()

    async def download_to_stream(self, stream, max_concurrency=1):
        """DEPRECATED: Download the contents of this blob to a stream.

        This method is deprecated, use func:`readinto` instead.

        :param IO[T] stream:
            The stream to download to. This can be an open file-handle,
            or any writable stream. The stream must be seekable if the download
            uses more than one parallel connection.
        :param int max_concurrency:
            The number of parallel connections with which to download.
        :returns: The properties of the downloaded blob.
        :rtype: Any
        """
        warnings.warn(
            "download_to_stream is deprecated, use readinto instead",
            DeprecationWarning
        )
        if self._text_mode:
            raise ValueError("Stream has been partially read in text mode. "
                             "download_to_stream is not supported in text mode.")

        self._max_concurrency = max_concurrency
        await self.readinto(stream)
        return self.properties
