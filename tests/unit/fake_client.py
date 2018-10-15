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

from huaweipythonsdkcore import client
from tests.unit import fake_authenticator
from huaweipythonsdkcore import endpoint_resolver


class FakeEndpointResolover(endpoint_resolver.EndpointResolver):

    def resolve(self, req, region, tenant=None):
        return "http://fake_host:fake_port/fake_service"


class Client(client.Client):

    def __init__(self, **kwargs):
        kwargs['authenticator'] = fake_authenticator.FakeAuthenticator()
        kwargs['resolver'] = FakeEndpointResolover()
        super(Client, self).__init__(**kwargs)
