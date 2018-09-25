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

import requests

from huaweipythonsdkcore import request as request
from huaweipythonsdkcore.sign import factory as sign_util
from huaweipythonsdkcore import utils
from huaweipythonsdkcore import request_handler
from huaweipythonsdkcore import endpoint_resolver
from huaweipythonsdkcore import exception


class Client(object):

    def __init__(self, auth_url=None, credential=None, region=None,
                 tenant=None):
        self.auth_url = auth_url
        self.credential = credential
        self.region = region
        # NOTE(tommylikehu): In most of the cases, the tenant would be equal
        # to region, therefore, we set it to region if parameter not provided.
        self.tenant = tenant if tenant else region
        self.signer = sign_util.get_signer(cred=credential, region=region)
        self.resolver = endpoint_resolver.HttpEndpointResolver(self.auth_url,
                                                               self.signer)
        self.handler = request_handler.RequestHandler.get_instance()

    def _do_request(self, req, endpoint):

        try:
            full_path = utils.get_request_endpoint(req, endpoint)
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
        except requests.exceptions.RequestException as err:
            raise exception.RequestException(err.message)

    def handle_request(self, req):
        if not isinstance(req, request.BaseRequest):
            raise exception.ValueException(
                "request must be an instance of 'BaseRequest'.")
        # Get service endpoint from endpoint resolver
        endpoint = self.resolver.resolve(req, self.region, self.tenant)
        return self._do_request(req, endpoint)
