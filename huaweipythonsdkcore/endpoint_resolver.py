# Copyright (c) 2018 Huawei Technologies Co., Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
from abc import ABCMeta, abstractmethod
import httplib

from huaweipythonsdkcore import request
from huaweipythonsdkcore import request_handler
from huaweipythonsdkcore import utils
from huaweipythonsdkcore import exception
from huaweipythonsdkcore import base_client


class EndpointResolver(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def resolve(self, req, region, tenant=None):
        pass


class AuthenticationRequest(request.BaseRequest):

    _service = 'identity'


class EndpointRequest(AuthenticationRequest):
    _base_endpoint = '/endpoints'
    _success_codes = httplib.OK


class ServiceRequest(AuthenticationRequest):
    _base_endpoint = '/services'
    _success_codes = httplib.OK


class ProjectRequest(AuthenticationRequest):
    _base_endpoint = '/projects'
    _success_codes = httplib.OK


class HttpEndpointResolver(EndpointResolver, base_client.BaseClient):

    TENANT_REGEX = '$(tenant_id)s'

    def __init__(self, auth_url, authenticator):
        self.auth_url = auth_url
        self.handler = request_handler.RequestHandler.get_instance()
        self.authenticator = authenticator
        self._endpoint_cache = {}
        super(HttpEndpointResolver, self).__init__(
            authenticator=self.authenticator)

    def _assemble_endpoint_with_tenant(self, tenant, endpoint):
        project_request = ProjectRequest()
        project_request.url_params = {'name': tenant}
        full_path = utils.get_request_endpoint(project_request, self.auth_url)
        _, result, _ = self._do_request(project_request, full_path)
        projects = json.loads(result)
        project_ids = [p['id'] for p in projects['projects']]
        return endpoint.replace(self.TENANT_REGEX, project_ids[0])

    def _resolve(self, req, region, tenant=None):
        # Collect service id from services response
        service_request = ServiceRequest()
        full_path = utils.get_request_endpoint(service_request, self.auth_url)
        _, result, _ = self._do_request(service_request, full_path)
        services = json.loads(result)
        service = [sv['id'] for sv in services['services']
                   if sv['name'] == req.service]
        if len(service) == 0:
            raise exception.EndpointResolveException(
                "Can't find service identified with name %s." % req.service)

        # Collect endpoint(s) via service id
        endpoint_request = EndpointRequest()
        full_path = utils.get_request_endpoint(endpoint_request, self.auth_url)
        _, result, _ = self._do_request(endpoint_request, full_path)
        endpoints = json.loads(result)
        endpoint = [ep['url'] for ep in endpoints['endpoints']
                    if (ep['interface'] == req.interface
                        and ep['service_id'] in service
                        and ('region' in ep and ep['region'] == region))]

        if len(endpoint) == 0:
            raise exception.EndpointResolveException(
                "Not any legal endpoint is founded with region %s." % region)
        if len(endpoint) >= 2:
            raise exception.EndpointResolveException(
                "Multiple legal endpoints are founded: %s "
                "with region %s." % (','.join(endpoint), region))
        # Convert path template into real one,
        # for example: 'http://host/server/$(tenant_id)s'
        request_endpoint = endpoint[0]
        if self.TENANT_REGEX in request_endpoint:
            request_endpoint = self._assemble_endpoint_with_tenant(
                tenant, request_endpoint)
        return request_endpoint

    def resolve(self, req, region, tenant=None):
        endpoint_key = "{}/{}/{}/{}".format(region, tenant,
                                            req.service, req.interface)
        if endpoint_key not in self._endpoint_cache:
            self._endpoint_cache[endpoint_key] = self._resolve(req, region,
                                                               tenant)
        return self._endpoint_cache[endpoint_key]
