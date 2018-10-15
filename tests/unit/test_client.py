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

from testtools import TestCase
import mock
import ssl
from huaweipythonsdkcore import configuration
from tests.unit import fake_client


class TestClass(TestCase):

    @mock.patch('urllib3.PoolManager.__init__')
    def test_initialize_client_with_object_ssl_false(self, mock_pool_manager):
        mock_pool_manager.return_value = None
        conf = configuration.Configuration(
            verify_ssl=False,
            pool_size=11,
            timeout=31,
            retries=12)
        _ = fake_client.Client(
            auth_url='Fake_url', credential='fake_credentical',
            region='fake_region',
            configuration=conf)

        mock_pool_manager.assert_called_with(
            num_pools=11,
            cert_reqs=ssl.CERT_NONE,
            retries=mock.ANY,
            timeout=31)

    @mock.patch('urllib3.PoolManager.__init__')
    def test_initialize_client_with_object_ssl_true(self,
                                                    mock_pool_manager):
        mock_pool_manager.return_value = None
        conf = configuration.Configuration(
            verify_ssl=True,
            ca_certs=['fake_file1', 'fake_file2'])
        default_conf = configuration.Configuration()
        _ = fake_client.Client(
            auth_url='Fake_url', credential='fake_credentical',
            region='fake_region',
            configuration=conf)

        mock_pool_manager.assert_called_with(
            num_pools=default_conf.pool_size,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs=['fake_file1', 'fake_file2'],
            retries=mock.ANY,
            timeout=default_conf.timeout)
