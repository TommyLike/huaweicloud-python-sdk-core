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

import testtools
from tests.functional import test_utils
from huaweipythonsdkcore import client
from huaweipythonsdkcore import credential
from tests.functional import test_aksk_credential


class PwdCredential(test_aksk_credential.AkSKCredential):

    def setUp(self):
        super(PwdCredential, self).setUp()
        self.client = client.Client(
            auth_url=os.environ['auth_url'],
            credential=credential.PasswordCredential(
                username=os.environ['username'],
                password=os.environ['password'],
                domain=os.environ['domain'],
                project=os.environ['region']),
            region=os.environ['region'])

    @testtools.skipIf(
        (test_utils.environments_exist(['auth_url', 'region',
                                        'username',
                                        'password',
                                        'domain']) is False),
        "PWD testcases skipped due to incomplete envs.")
    def test_list_volume(self):
        super(PwdCredential, self).test_list_volume()

    @testtools.skipIf(
        (test_utils.environments_exist(['auth_url', 'region',
                                        'username',
                                        'password',
                                        'domain']) is False),
        "PWD testcases skipped due to incomplete envs.")
    def test_volume_crud(self):
        super(PwdCredential, self).test_volume_crud()
