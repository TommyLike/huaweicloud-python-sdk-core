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

from huaweipythonsdkcore import configuration


class TestConfigurations(TestCase):

    def test_initialize_with_known_attributes(self):

        conf = configuration.Configuration(**{
            'retries': 100,
            'timeout': 1024
        })
        default_conf = configuration.Configuration()
        for value, attribute in [(default_conf.verify_ssl, conf.verify_ssl),
                                 (default_conf.ca_certs, conf.ca_certs),
                                 (100, conf.retries),
                                 (1024, conf.timeout)]:
            self.assertEqual(value, attribute)

    def test_initialize_with_unkown_attributes(self):
        conf = configuration.Configuration(**{
            'attribute1': 'value1',
            'attribute2': 'value2'
        })
        default_conf = configuration.Configuration()
        for value, attribute in [(default_conf.verify_ssl, conf.verify_ssl),
                                 (default_conf.ca_certs, conf.ca_certs),
                                 (default_conf.retries, conf.retries),
                                 (default_conf.timeout, conf.timeout)]:
            self.assertEqual(value, attribute)

