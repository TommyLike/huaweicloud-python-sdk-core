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


class HttpEndpointResolver(EndpointResolver):

    TENANT_REGEX = '$(tenant_id)s'

    def __init__(self, auth_url, signer):
        self.auth_url = auth_url
        self.handler = request_handler.RequestHandler.get_instance()
        self.signer = signer
        self._endpoint_cache = {}

    def _do_request(self, req):

        full_path = utils.get_request_endpoint(req, self.auth_url)
        headers = utils.collect_complete_headers(full_path, req)

        headers = self.signer.sign(
            full_path, req.http_method, headers,
            body=req.body, params=req.url_params, service=req.service)
        return self.handler.handle_request(path=full_path,
                                           method=req.http_method,
                                           headers=headers,
                                           url_params=req.url_params,
                                           body=req.body,
                                           timeout=req.timeout,
                                           expected_code=req.success_code)

    def _assemble_endpoint_with_tenant(self, tenant, endpoint):
        project_request = ProjectRequest()
        project_request.url_params = {'name': tenant}
        result = self._do_request(project_request)
        projects = json.loads(result)
        project_ids = [p['id'] for p in projects['projects']]
        return endpoint.replace(self.TENANT_REGEX, project_ids[0])

    def _resolve(self, req, region, tenant=None):
        # Collect service id from services response
        service_request = ServiceRequest()
        result = self._do_request(service_request)
        services = json.loads(result)
        service = [sv['id'] for sv in services['services']
                   if sv['name'] == req.service]
        if len(service) == 0:
            raise exception.EndpointResolveException(
                "Can't find service identified with name %s." % req.service)

        # Collect endpoint(s) via service id
        endpoint_request = EndpointRequest()
        result = self._do_request(endpoint_request)
        endpoints = json.loads(result)
        endpoint = [ep['url'] for ep in endpoints['endpoints']
                    if (ep['interface'] == req.interface
                        and ep['service_id'] in service
                        and ('region' in ep and ep['region'] == region))]

        if len(endpoint) == 0 or len(endpoint) >= 2:
            raise exception.EndpointResolveException(
                "Multiple legal endpoints are founded.")
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
        if not self._endpoint_cache.has_key(endpoint_key):
            self._endpoint_cache[endpoint_key] = self._resolve(req, region,
                                                               tenant)
        return self._endpoint_cache[endpoint_key]
