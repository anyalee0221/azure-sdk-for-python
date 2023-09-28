# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING

from msrest import Serializer

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    map_error,
)
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from .._vendor import _convert_request, _format_url_section

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar
    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False
# fmt: off

def build_list_request(
    subscription_id,  # type: str
    resource_group_name,  # type: str
    workspace_name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
    skip = kwargs.pop('skip', None)  # type: Optional[str]
    count = kwargs.pop('count', 30)  # type: Optional[int]
    is_default = kwargs.pop('is_default', None)  # type: Optional[bool]
    names = kwargs.pop('names', None)  # type: Optional[List[str]]
    search_text = kwargs.pop('search_text', None)  # type: Optional[str]
    order_by = kwargs.pop('order_by', None)  # type: Optional[str]
    order_by_asc = kwargs.pop('order_by_asc', False)  # type: Optional[bool]

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', min_length=1),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1),
        "workspaceName": _SERIALIZER.url("workspace_name", workspace_name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{2,32}$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')
    if skip is not None:
        _query_parameters['$skip'] = _SERIALIZER.query("skip", skip, 'str')
    if count is not None:
        _query_parameters['count'] = _SERIALIZER.query("count", count, 'int')
    if is_default is not None:
        _query_parameters['isDefault'] = _SERIALIZER.query("is_default", is_default, 'bool')
    if names is not None:
        _query_parameters['names'] = _SERIALIZER.query("names", names, '[str]', div=',')
    if search_text is not None:
        _query_parameters['searchText'] = _SERIALIZER.query("search_text", search_text, 'str')
    if order_by is not None:
        _query_parameters['orderBy'] = _SERIALIZER.query("order_by", order_by, 'str')
    if order_by_asc is not None:
        _query_parameters['orderByAsc'] = _SERIALIZER.query("order_by_asc", order_by_asc, 'bool')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_delete_request(
    subscription_id,  # type: str
    resource_group_name,  # type: str
    workspace_name,  # type: str
    name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', min_length=1),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1),
        "workspaceName": _SERIALIZER.url("workspace_name", workspace_name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{2,32}$'),
        "name": _SERIALIZER.url("name", name, 'str'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="DELETE",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_get_request(
    subscription_id,  # type: str
    resource_group_name,  # type: str
    workspace_name,  # type: str
    name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', min_length=1),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1),
        "workspaceName": _SERIALIZER.url("workspace_name", workspace_name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{2,32}$'),
        "name": _SERIALIZER.url("name", name, 'str'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_create_or_update_request(
    subscription_id,  # type: str
    resource_group_name,  # type: str
    workspace_name,  # type: str
    name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]
    skip_validation = kwargs.pop('skip_validation', False)  # type: Optional[bool]

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', min_length=1),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1),
        "workspaceName": _SERIALIZER.url("workspace_name", workspace_name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{2,32}$'),
        "name": _SERIALIZER.url("name", name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9\-_]{0,254}$'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')
    if skip_validation is not None:
        _query_parameters['skipValidation'] = _SERIALIZER.query("skip_validation", skip_validation, 'bool')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        _header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="PUT",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )


def build_list_secrets_request(
    subscription_id,  # type: str
    resource_group_name,  # type: str
    workspace_name,  # type: str
    name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}/listSecrets")  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, 'str', min_length=1),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1),
        "workspaceName": _SERIALIZER.url("workspace_name", workspace_name, 'str', pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{2,32}$'),
        "name": _SERIALIZER.url("name", name, 'str'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="POST",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )

# fmt: on
class DatastoresOperations(object):
    """DatastoresOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.machinelearningservices.models
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

    @distributed_trace
    def list(
        self,
        resource_group_name,  # type: str
        workspace_name,  # type: str
        skip=None,  # type: Optional[str]
        count=30,  # type: Optional[int]
        is_default=None,  # type: Optional[bool]
        names=None,  # type: Optional[List[str]]
        search_text=None,  # type: Optional[str]
        order_by=None,  # type: Optional[str]
        order_by_asc=False,  # type: Optional[bool]
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["_models.DatastoreResourceArmPaginatedResult"]
        """List datastores.

        List datastores.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param skip: Continuation token for pagination.
        :type skip: str
        :param count: Maximum number of results to return.
        :type count: int
        :param is_default: Filter down to the workspace default datastore.
        :type is_default: bool
        :param names: Names of datastores to return.
        :type names: list[str]
        :param search_text: Text to search for in the datastore names.
        :type search_text: str
        :param order_by: Order by property (createdtime | modifiedtime | name).
        :type order_by: str
        :param order_by_asc: Order by property in ascending order.
        :type order_by_asc: bool
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either DatastoreResourceArmPaginatedResult or the result
         of cls(response)
        :rtype:
         ~azure.core.paging.ItemPaged[~azure.mgmt.machinelearningservices.models.DatastoreResourceArmPaginatedResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.DatastoreResourceArmPaginatedResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    workspace_name=workspace_name,
                    api_version=api_version,
                    skip=skip,
                    count=count,
                    is_default=is_default,
                    names=names,
                    search_text=search_text,
                    order_by=order_by,
                    order_by_asc=order_by_asc,
                    template_url=self.list.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    workspace_name=workspace_name,
                    api_version=api_version,
                    skip=skip,
                    count=count,
                    is_default=is_default,
                    names=names,
                    search_text=search_text,
                    order_by=order_by,
                    order_by_asc=order_by_asc,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize("DatastoreResourceArmPaginatedResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response


        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores"}  # type: ignore

    @distributed_trace
    def delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name,  # type: str
        workspace_name,  # type: str
        name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Delete datastore.

        Delete datastore.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param name: Datastore name.
        :type name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        
        request = build_delete_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            name=name,
            api_version=api_version,
            template_url=self.delete.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}"}  # type: ignore


    @distributed_trace
    def get(
        self,
        resource_group_name,  # type: str
        workspace_name,  # type: str
        name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.Datastore"
        """Get datastore.

        Get datastore.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param name: Datastore name.
        :type name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Datastore, or the result of cls(response)
        :rtype: ~azure.mgmt.machinelearningservices.models.Datastore
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Datastore"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        
        request = build_get_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            name=name,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Datastore', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}"}  # type: ignore


    @distributed_trace
    def create_or_update(
        self,
        resource_group_name,  # type: str
        workspace_name,  # type: str
        name,  # type: str
        body,  # type: "_models.Datastore"
        skip_validation=False,  # type: Optional[bool]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.Datastore"
        """Create or update datastore.

        Create or update datastore.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param name: Datastore name.
        :type name: str
        :param body: Datastore entity to create or update.
        :type body: ~azure.mgmt.machinelearningservices.models.Datastore
        :param skip_validation: Flag to skip validation.
        :type skip_validation: bool
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Datastore, or the result of cls(response)
        :rtype: ~azure.mgmt.machinelearningservices.models.Datastore
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Datastore"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(body, 'Datastore')

        request = build_create_or_update_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            name=name,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            skip_validation=skip_validation,
            template_url=self.create_or_update.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('Datastore', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('Datastore', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_or_update.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}"}  # type: ignore


    @distributed_trace
    def list_secrets(
        self,
        resource_group_name,  # type: str
        workspace_name,  # type: str
        name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.DatastoreSecrets"
        """Get datastore secrets.

        Get datastore secrets.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param name: Datastore name.
        :type name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: DatastoreSecrets, or the result of cls(response)
        :rtype: ~azure.mgmt.machinelearningservices.models.DatastoreSecrets
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.DatastoreSecrets"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-10-01")  # type: str

        
        request = build_list_secrets_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            name=name,
            api_version=api_version,
            template_url=self.list_secrets.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('DatastoreSecrets', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_secrets.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/datastores/{name}/listSecrets"}  # type: ignore

