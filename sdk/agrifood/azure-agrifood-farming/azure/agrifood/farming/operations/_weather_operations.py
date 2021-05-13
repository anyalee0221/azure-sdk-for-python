# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import datetime
from typing import TYPE_CHECKING
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpRequest, HttpResponse
from azure.core.polling import LROPoller, NoPolling, PollingMethod
from azure.core.polling.base_polling import LROBasePolling

from .. import models as _models

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, Iterable, Optional, TypeVar, Union

    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

class WeatherOperations(object):
    """WeatherOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.agrifood.farming.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def list(
        self,
        farmer_id,  # type: str
        boundary_id,  # type: str
        extension_id,  # type: str
        weather_data_type,  # type: str
        granularity,  # type: str
        start_date_time=None,  # type: Optional[datetime.datetime]
        end_date_time=None,  # type: Optional[datetime.datetime]
        max_page_size=50,  # type: Optional[int]
        skip_token=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["_models.WeatherDataListResponse"]
        """Returns a paginated list of weather data.

        :param farmer_id: Farmer ID.
        :type farmer_id: str
        :param boundary_id: Boundary ID.
        :type boundary_id: str
        :param extension_id: ID of the weather extension.
        :type extension_id: str
        :param weather_data_type: Type of weather data (forecast/historical).
        :type weather_data_type: str
        :param granularity: Granularity of weather data (daily/hourly).
        :type granularity: str
        :param start_date_time: Weather data start UTC date-time (inclusive), sample format:
         yyyy-MM-ddTHH:mm:ssZ.
        :type start_date_time: ~datetime.datetime
        :param end_date_time: Weather data end UTC date-time (inclusive), sample format:
         yyyy-MM-ddTHH:mm:ssZ.
        :type end_date_time: ~datetime.datetime
        :param max_page_size: Maximum number of items needed (inclusive).
         Minimum = 10, Maximum = 1000, Default value = 50.
        :type max_page_size: int
        :param skip_token: Skip token for getting next set of results.
        :type skip_token: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either WeatherDataListResponse or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.agrifood.farming.models.WeatherDataListResponse]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataListResponse"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2021-03-31-preview"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list.metadata['url']  # type: ignore
                path_format_arguments = {
                    'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['farmerId'] = self._serialize.query("farmer_id", farmer_id, 'str')
                query_parameters['boundaryId'] = self._serialize.query("boundary_id", boundary_id, 'str')
                query_parameters['extensionId'] = self._serialize.query("extension_id", extension_id, 'str', pattern=r'^[A-za-z]{3,50}[.][A-za-z]{3,100}$')
                query_parameters['weatherDataType'] = self._serialize.query("weather_data_type", weather_data_type, 'str', max_length=50, min_length=0)
                query_parameters['granularity'] = self._serialize.query("granularity", granularity, 'str', max_length=50, min_length=0)
                if start_date_time is not None:
                    query_parameters['startDateTime'] = self._serialize.query("start_date_time", start_date_time, 'iso-8601')
                if end_date_time is not None:
                    query_parameters['endDateTime'] = self._serialize.query("end_date_time", end_date_time, 'iso-8601')
                if max_page_size is not None:
                    query_parameters['$maxPageSize'] = self._serialize.query("max_page_size", max_page_size, 'int', maximum=1000, minimum=10)
                if skip_token is not None:
                    query_parameters['$skipToken'] = self._serialize.query("skip_token", skip_token, 'str')
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                path_format_arguments = {
                    'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
                }
                url = self._client.format_url(url, **path_format_arguments)
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('WeatherDataListResponse', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, response)
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, model=error)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': '/weather'}  # type: ignore

    def get_data_ingestion_job_details(
        self,
        job_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.WeatherDataIngestionJob"
        """Get weather ingestion job.

        :param job_id: Id of the job.
        :type job_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: WeatherDataIngestionJob, or the result of cls(response)
        :rtype: ~azure.agrifood.farming.models.WeatherDataIngestionJob
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataIngestionJob"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2021-03-31-preview"
        accept = "application/json"

        # Construct URL
        url = self.get_data_ingestion_job_details.metadata['url']  # type: ignore
        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('WeatherDataIngestionJob', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get_data_ingestion_job_details.metadata = {'url': '/weather/ingest-data/{jobId}'}  # type: ignore

    def _create_data_ingestion_job_initial(
        self,
        job_id,  # type: str
        body=None,  # type: Optional["_models.WeatherDataIngestionJob"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.WeatherDataIngestionJob"
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataIngestionJob"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2021-03-31-preview"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self._create_data_ingestion_job_initial.metadata['url']  # type: ignore
        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        if body is not None:
            body_content = self._serialize.body(body, 'WeatherDataIngestionJob')
        else:
            body_content = None
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('WeatherDataIngestionJob', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    _create_data_ingestion_job_initial.metadata = {'url': '/weather/ingest-data/{jobId}'}  # type: ignore

    def begin_create_data_ingestion_job(
        self,
        job_id,  # type: str
        body=None,  # type: Optional["_models.WeatherDataIngestionJob"]
        **kwargs  # type: Any
    ):
        # type: (...) -> LROPoller["_models.WeatherDataIngestionJob"]
        """Create a weather data ingestion job.

        :param job_id: Job id supplied by user.
        :type job_id: str
        :param body: Job parameters supplied by user.
        :type body: ~azure.agrifood.farming.models.WeatherDataIngestionJob
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be LROBasePolling.
         Pass in False for this operation to not poll, or pass in your own initialized polling object for a personal polling strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
        :return: An instance of LROPoller that returns either WeatherDataIngestionJob or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.agrifood.farming.models.WeatherDataIngestionJob]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataIngestionJob"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = self._create_data_ingestion_job_initial(
                job_id=job_id,
                body=body,
                cls=lambda x,y,z: x,
                **kwargs
            )

        kwargs.pop('error_map', None)
        kwargs.pop('content_type', None)

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize('WeatherDataIngestionJob', pipeline_response)

            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }

        if polling is True: polling_method = LROBasePolling(lro_delay, lro_options={'final-state-via': 'location'}, path_format_arguments=path_format_arguments,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        else:
            return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_create_data_ingestion_job.metadata = {'url': '/weather/ingest-data/{jobId}'}  # type: ignore

    def get_data_delete_job_details(
        self,
        job_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.WeatherDataDeleteJob"
        """Get weather data delete job.

        :param job_id: Id of the job.
        :type job_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: WeatherDataDeleteJob, or the result of cls(response)
        :rtype: ~azure.agrifood.farming.models.WeatherDataDeleteJob
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataDeleteJob"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2021-03-31-preview"
        accept = "application/json"

        # Construct URL
        url = self.get_data_delete_job_details.metadata['url']  # type: ignore
        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('WeatherDataDeleteJob', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get_data_delete_job_details.metadata = {'url': '/weather/delete-data/{jobId}'}  # type: ignore

    def _create_data_delete_job_initial(
        self,
        job_id,  # type: str
        body=None,  # type: Optional["_models.WeatherDataDeleteJob"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.WeatherDataDeleteJob"
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataDeleteJob"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2021-03-31-preview"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self._create_data_delete_job_initial.metadata['url']  # type: ignore
        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        if body is not None:
            body_content = self._serialize.body(body, 'WeatherDataDeleteJob')
        else:
            body_content = None
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('WeatherDataDeleteJob', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    _create_data_delete_job_initial.metadata = {'url': '/weather/delete-data/{jobId}'}  # type: ignore

    def begin_create_data_delete_job(
        self,
        job_id,  # type: str
        body=None,  # type: Optional["_models.WeatherDataDeleteJob"]
        **kwargs  # type: Any
    ):
        # type: (...) -> LROPoller["_models.WeatherDataDeleteJob"]
        """Create a weather data delete job.

        :param job_id: Job Id supplied by end user.
        :type job_id: str
        :param body: Job parameters supplied by user.
        :type body: ~azure.agrifood.farming.models.WeatherDataDeleteJob
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be LROBasePolling.
         Pass in False for this operation to not poll, or pass in your own initialized polling object for a personal polling strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
        :return: An instance of LROPoller that returns either WeatherDataDeleteJob or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.agrifood.farming.models.WeatherDataDeleteJob]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.WeatherDataDeleteJob"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = self._create_data_delete_job_initial(
                job_id=job_id,
                body=body,
                cls=lambda x,y,z: x,
                **kwargs
            )

        kwargs.pop('error_map', None)
        kwargs.pop('content_type', None)

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize('WeatherDataDeleteJob', pipeline_response)

            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        path_format_arguments = {
            'Endpoint': self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
            'jobId': self._serialize.url("job_id", job_id, 'str'),
        }

        if polling is True: polling_method = LROBasePolling(lro_delay, lro_options={'final-state-via': 'location'}, path_format_arguments=path_format_arguments,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        else:
            return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_create_data_delete_job.metadata = {'url': '/weather/delete-data/{jobId}'}  # type: ignore
