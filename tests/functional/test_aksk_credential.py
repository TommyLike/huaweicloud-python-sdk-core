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

import os
import json

from testtools import TestCase
from huaweipythonsdkcore import request
from huaweipythonsdkcore import client
from huaweipythonsdkcore import credential


class CreateVolumeRequest(request.BaseRequest):

    _base_endpoint = '/volumes'

    _http_method = 'POST'

    _service = 'evs'

    _user_agent = 'huaweicloud-sdk-core-functional-test'

    def __init__(self, name, description, size, volume_type):
        body = {'volume': {'name': name,
                           'description': description,
                           'size': size,
                           'volume_type': volume_type}}
        super(CreateVolumeRequest, self).__init__(body=body)


class ListVolumeRequest(request.BaseRequest):

    _base_endpoint = '/volumes'

    _http_method = 'GET'

    _service = 'evs'

    _user_agent = 'huaweicloud-sdk-core-functional-test'


class AkSKCredential(TestCase):

    def setUp(self):
        super(AkSKCredential, self).setUp()
        self.client = client.Client(
            auth_url=os.environ['auth_url'],
            credential=credential.AccessKeyCredential(
                access_key_id=os.environ['access_key_id'],
                access_key_secret=os.environ['access_key_secret']
            ),
            region=os.environ['region'])

    def test_create_volume(self):
        create_volume = CreateVolumeRequest(
            name='Python-Core-Functional-Test',
            description='fake description',
            size=1,
            volume_type='SATA')
        code, result, _ = self.client.handle_request(req=create_volume)
        self.assertEqual(202, code,
                         "Volume should created via Created response,")

    def test_list_volume(self):
        code, result, _ = self.client.handle_request(req=ListVolumeRequest())
        self.assertEqual(200, code,
                         "List volume should return OK status code.")
        volumes = json.loads(result)
        self.assertIsInstance(volumes['volumes'], list)
