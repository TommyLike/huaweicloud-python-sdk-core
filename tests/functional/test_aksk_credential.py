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

import testtools
from testtools import TestCase
from tests.functional import test_utils
from huaweipythonsdkcore import request
from huaweipythonsdkcore import client
from huaweipythonsdkcore import credential


class EvsRequest(request.BaseRequest):

    _service = 'evs'

    _user_agent = 'huaweicloud-sdk-core-functional-test'


class CreateVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes'

    _http_method = 'POST'

    def __init__(self, name, description, size, volume_type):
        body = {'volume': {'name': name,
                           'description': description,
                           'size': size,
                           'volume_type': volume_type}}
        super(CreateVolumeRequest, self).__init__(body=body)


class ListVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes'

    _http_method = 'GET'


class ShowVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'GET'

    def __init__(self, volume_id):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        super(ShowVolumeRequest, self).__init__()


class UpdateVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'PUT'

    _available_attributes = {
        'Name': str,
        'Description': str,
        'Size': int,
        'Volume_Type': str
    }

    def __init__(self, volume_id, name=None, description=None, size=None,
                 volume_type=None):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        body = {'volume': {'name': name,
                           'description': description,
                           'size': size,
                           'volume_type': volume_type}}
        super(UpdateVolumeRequest, self).__init__(body=body)

    def __getattr__(self, item):
        if item in self._available_attributes:
            return self.body['volume'][item.lower()]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self._available_attributes:
            if not isinstance(value, self._available_attributes[key]):
                raise ValueError("{} should be an instance of {}".format(
                    key, self._available_attributes[key]))
            self.body['volume'][key.lower()] = value
        else:
            super(UpdateVolumeRequest, self).__setattr__(key, value)


class DeleteVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'DELETE'

    def __init__(self, volume_id):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        super(DeleteVolumeRequest, self).__init__()


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

    @testtools.skipIf(
        (test_utils.environments_exist(['auth_url', 'region',
                                        'access_key_id',
                                        'access_key_secret']) is False),
        "AKSK testcases skipped due to incomplete envs.")
    def test_list_volume(self):
        code, result, _ = self.client.handle_request(req=ListVolumeRequest())
        self.assertEqual(200, code,
                         "List volume should return OK status code.")
        volumes = json.loads(result)
        self.assertIsInstance(volumes['volumes'], list)

    @testtools.skipIf(
        (test_utils.environments_exist(['auth_url', 'region',
                                        'access_key_id',
                                        'access_key_secret']) is False),
        "AKSK testcases skipped due to incomplete envs.")
    def test_volume_crud(self):
        # create volume
        create_volume = CreateVolumeRequest(
            name='Python-Core-Functional-Test',
            description='fake description',
            size=1,
            volume_type='SATA')
        code, result, _ = self.client.handle_request(req=create_volume)
        self.assertEqual(202, code,
                         "Create volume should return 202 code.")

        # show volume
        volume = json.loads(result)
        while volume['volume']['status'] != 'available':
            show_volume = ShowVolumeRequest(volume['volume']['id'])
            code, result, _ = self.client.handle_request(req=show_volume)
            self.assertEqual(200, code,
                             "Show volume should return 200 code.")
            volume = json.loads(result)

        # Update volume
        new_name = "this the new name"
        update_volume = UpdateVolumeRequest(volume['volume']['id'])
        update_volume.Name = new_name
        code, result, _ = self.client.handle_request(req=update_volume)
        self.assertEqual(code, 200, "Update volume should return 200 code.")
        new_volume = json.loads(result)
        self.assertEqual(
            new_name, new_volume['volume']['name'],
            "Updated volume's name should be equal to %s." % new_volume)

        # Delete volume
        delete_volume = DeleteVolumeRequest(volume['volume']['id'])
        code, _, _ = self.client.handle_request(req=delete_volume)
        self.assertEqual(202, code, "Delete volume should return 202 code.")
