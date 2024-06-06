# pylint: disable=too-many-lines,too-many-statements
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import sys
from typing import Any, Callable, Dict, List, Literal, Optional, Type, TypeVar

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict

from .. import models as _models
from .._serialization import Serializer
from .._vendor import _convert_request

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore  # pylint: disable=ungrouped-imports
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_create_request(
    url: str,
    *,
    timeout: Optional[int] = None,
    metadata: Optional[Dict[str, str]] = None,
    request_id_parameter: Optional[str] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    if metadata is not None:
        _headers["x-ms-meta"] = _SERIALIZER.header("metadata", metadata, "{str}")
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PUT", url=_url, params=_params, headers=_headers, **kwargs)


def build_delete_request(
    url: str, *, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="DELETE", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_properties_request(
    url: str, *, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    comp: Literal["metadata"] = kwargs.pop("comp", _params.pop("comp", "metadata"))
    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["comp"] = _SERIALIZER.query("comp", comp, "str")
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_set_metadata_request(
    url: str,
    *,
    timeout: Optional[int] = None,
    metadata: Optional[Dict[str, str]] = None,
    request_id_parameter: Optional[str] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    comp: Literal["metadata"] = kwargs.pop("comp", _params.pop("comp", "metadata"))
    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["comp"] = _SERIALIZER.query("comp", comp, "str")
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    if metadata is not None:
        _headers["x-ms-meta"] = _SERIALIZER.header("metadata", metadata, "{str}")
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PUT", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_access_policy_request(
    url: str, *, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    comp: Literal["acl"] = kwargs.pop("comp", _params.pop("comp", "acl"))
    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["comp"] = _SERIALIZER.query("comp", comp, "str")
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_set_access_policy_request(
    url: str,
    *,
    timeout: Optional[int] = None,
    request_id_parameter: Optional[str] = None,
    content: Any = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    comp: Literal["acl"] = kwargs.pop("comp", _params.pop("comp", "acl"))
    content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
    version: Literal["2018-03-28"] = kwargs.pop("version", _headers.pop("x-ms-version", "2018-03-28"))
    accept = _headers.pop("Accept", "application/xml")

    # Construct URL
    _url = kwargs.pop("template_url", "{url}")
    path_format_arguments = {
        "url": _SERIALIZER.url("url", url, "str", skip_quote=True),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["comp"] = _SERIALIZER.query("comp", comp, "str")
    if timeout is not None:
        _params["timeout"] = _SERIALIZER.query("timeout", timeout, "int", minimum=0)

    # Construct headers
    _headers["x-ms-version"] = _SERIALIZER.header("version", version, "str")
    if request_id_parameter is not None:
        _headers["x-ms-client-request-id"] = _SERIALIZER.header("request_id_parameter", request_id_parameter, "str")
    if content_type is not None:
        _headers["Content-Type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PUT", url=_url, params=_params, headers=_headers, content=content, **kwargs)


class QueueOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.storage.queue.AzureQueueStorage`'s
        :attr:`queue` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def create(  # pylint: disable=inconsistent-return-statements
        self,
        timeout: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        request_id_parameter: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """creates a new queue under the given account.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param metadata: Optional. Include this parameter to specify that the queue's metadata be
         returned as part of the response body. Note that metadata requested with this parameter must be
         stored in accordance with the naming restrictions imposed by the 2009-09-19 version of the
         Queue service. Beginning with this version, all metadata names must adhere to the naming
         conventions for C# identifiers. Default value is None.
        :type metadata: dict[str, str]
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_create_request(
            url=self._config.url,
            timeout=timeout,
            metadata=metadata,
            request_id_parameter=request_id_parameter,
            version=self._config.version,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [201, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        if response.status_code == 201:
            response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
            response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
            response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if response.status_code == 204:
            response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
            response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
            response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if cls:
            return cls(pipeline_response, None, response_headers)  # type: ignore

    @distributed_trace
    def delete(  # pylint: disable=inconsistent-return-statements
        self, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
    ) -> None:
        """operation permanently deletes the specified queue.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_delete_request(
            url=self._config.url,
            timeout=timeout,
            request_id_parameter=request_id_parameter,
            version=self._config.version,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
        response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
        response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if cls:
            return cls(pipeline_response, None, response_headers)  # type: ignore

    @distributed_trace
    def get_properties(  # pylint: disable=inconsistent-return-statements
        self, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Retrieves user-defined metadata and queue properties on the specified queue. Metadata is
        associated with the queue as name-values pairs.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        comp: Literal["metadata"] = kwargs.pop("comp", _params.pop("comp", "metadata"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_get_properties_request(
            url=self._config.url,
            timeout=timeout,
            request_id_parameter=request_id_parameter,
            comp=comp,
            version=self._config.version,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        response_headers["x-ms-meta"] = self._deserialize("{str}", response.headers.get("x-ms-meta"))
        response_headers["x-ms-approximate-messages-count"] = self._deserialize(
            "int", response.headers.get("x-ms-approximate-messages-count")
        )
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
        response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
        response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if cls:
            return cls(pipeline_response, None, response_headers)  # type: ignore

    @distributed_trace
    def set_metadata(  # pylint: disable=inconsistent-return-statements
        self,
        timeout: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        request_id_parameter: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """sets user-defined metadata on the specified queue. Metadata is associated with the queue as
        name-value pairs.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param metadata: Optional. Include this parameter to specify that the queue's metadata be
         returned as part of the response body. Note that metadata requested with this parameter must be
         stored in accordance with the naming restrictions imposed by the 2009-09-19 version of the
         Queue service. Beginning with this version, all metadata names must adhere to the naming
         conventions for C# identifiers. Default value is None.
        :type metadata: dict[str, str]
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        comp: Literal["metadata"] = kwargs.pop("comp", _params.pop("comp", "metadata"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_set_metadata_request(
            url=self._config.url,
            timeout=timeout,
            metadata=metadata,
            request_id_parameter=request_id_parameter,
            comp=comp,
            version=self._config.version,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
        response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
        response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if cls:
            return cls(pipeline_response, None, response_headers)  # type: ignore

    @distributed_trace
    def get_access_policy(
        self, timeout: Optional[int] = None, request_id_parameter: Optional[str] = None, **kwargs: Any
    ) -> List[_models.SignedIdentifier]:
        """returns details about any stored access policies specified on the queue that may be used with
        Shared Access Signatures.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :return: list of SignedIdentifier or the result of cls(response)
        :rtype: list[~azure.storage.queue.models.SignedIdentifier]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        comp: Literal["acl"] = kwargs.pop("comp", _params.pop("comp", "acl"))
        cls: ClsType[List[_models.SignedIdentifier]] = kwargs.pop("cls", None)

        _request = build_get_access_policy_request(
            url=self._config.url,
            timeout=timeout,
            request_id_parameter=request_id_parameter,
            comp=comp,
            version=self._config.version,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
        response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
        response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        deserialized = self._deserialize("[SignedIdentifier]", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, response_headers)  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace
    def set_access_policy(  # pylint: disable=inconsistent-return-statements
        self,
        timeout: Optional[int] = None,
        request_id_parameter: Optional[str] = None,
        queue_acl: Optional[List[_models.SignedIdentifier]] = None,
        **kwargs: Any
    ) -> None:
        """sets stored access policies for the queue that may be used with Shared Access Signatures.

        :param timeout: The The timeout parameter is expressed in seconds. For more information, see <a
         href="https://docs.microsoft.com/en-us/rest/api/storageservices/setting-timeouts-for-queue-service-operations>Setting
         Timeouts for Queue Service Operations.</a>. Default value is None.
        :type timeout: int
        :param request_id_parameter: Provides a client-generated, opaque value with a 1 KB character
         limit that is recorded in the analytics logs when storage analytics logging is enabled. Default
         value is None.
        :type request_id_parameter: str
        :param queue_acl: the acls for the queue. Default value is None.
        :type queue_acl: list[~azure.storage.queue.models.SignedIdentifier]
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        comp: Literal["acl"] = kwargs.pop("comp", _params.pop("comp", "acl"))
        content_type: str = kwargs.pop("content_type", _headers.pop("Content-Type", "application/xml"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        serialization_ctxt = {"xml": {"name": "SignedIdentifiers", "wrapped": True}}
        if queue_acl is not None:
            _content = self._serialize.body(
                queue_acl, "[SignedIdentifier]", is_xml=True, serialization_ctxt=serialization_ctxt
            )
        else:
            _content = None

        _request = build_set_access_policy_request(
            url=self._config.url,
            timeout=timeout,
            request_id_parameter=request_id_parameter,
            comp=comp,
            content_type=content_type,
            version=self._config.version,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request = _convert_request(_request)
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.StorageError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        response_headers = {}
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))
        response_headers["x-ms-version"] = self._deserialize("str", response.headers.get("x-ms-version"))
        response_headers["Date"] = self._deserialize("rfc-1123", response.headers.get("Date"))

        if cls:
            return cls(pipeline_response, None, response_headers)  # type: ignore
