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

from huaweipythonsdkcore import request as request
from huaweipythonsdkcore.auth import factory as sign_util
from huaweipythonsdkcore import utils
from huaweipythonsdkcore import endpoint_resolver
from huaweipythonsdkcore import exception
from huaweipythonsdkcore import base_client


class Client(base_client.BaseClient):

    def __init__(self, auth_url=None, credential=None, region=None,
                 tenant=None):
        self.auth_url = auth_url
        self.credential = credential
        self.region = region
        # NOTE(tommylikehu): In most of the cases, the tenant would be equal
        # to region, therefore, we set it to region if parameter not provided.
        self.tenant = tenant if tenant else region
        self.authenticator = sign_util.get_authenticator(
            cred=credential,
            region=region,
            auth_url=self.auth_url)
        self.resolver = endpoint_resolver.HttpEndpointResolver(
            self.auth_url,
            self.authenticator)
        super(Client, self).__init__(authenticator=self.authenticator)

    def handle_request(self, req):
        """Perform http request with supplied Request object

        :param req: Request object, is a instance of BaseRequest.
        :return: Response tuple, (code, content).
        :raise: SDKException: All of the exceptional cases are wrapped
                              in SDKException.
        """

        if not isinstance(req, request.BaseRequest):
            raise exception.ValueException(
                "request must be an instance of 'BaseRequest'.")
        # Get service endpoint from endpoint resolver
        endpoint = self.resolver.resolve(req, self.region, self.tenant)
        full_path = utils.get_request_endpoint(req, endpoint)
        return self._do_request(req, full_path)
