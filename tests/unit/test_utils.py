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

import ddt
from testtools import TestCase

from huaweipythonsdkcore import exception
from huaweipythonsdkcore import utils


@ddt.ddt
class TestUtils(TestCase):

    @ddt.data(
        {
            'headers': "",
            'body': {},
            'query_params': {},
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': "",
            'query_params': {},
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': {},
            'query_params': "",
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': {},
            'query_params': {},
            'service': '',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': {},
            'query_params': {},
            'service': None,
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': {},
            'query_params': {},
            'service': 'compute',
            'method': 'Deletes',
            'path': '/',
            'timeout': 1},
        {
            'headers': {},
            'body': {},
            'query_params': {},
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1.2},
        {
            'headers': "1111111111111",
            'body': {},
            'query_params': {},
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': "2222222222",
            'body': None,
            'query_params': None,
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1}
    )
    def test_build_request_object_invalid(self, param):
        self.assertRaises(exception.ValueException,
                          utils.build_request_object, **param)

    @ddt.data(
        {
            'headers': {'headers': "value"},
            'body': {},
            'query_params': {},
            'service': 'compute',
            'method': 'GET',
            'path': '/',
            'timeout': 1},
        {
            'headers': None,
            'body': None,
            'query_params': None,
            'service': 'compute',
            'method': 'get',
            'path': '/',
            'timeout': 1}
    )
    def test_build_request_object(self, param):
        result = utils.build_request_object(**param)
        self.assertEqual(result.service, param['service'])
        self.assertEqual(result.timeout, param['timeout'])
        self.assertEqual(result.headers,
                         {} if not param['headers'] else param['headers'])
        self.assertEqual(result.body,
                         {} if not param['body'] else param['body'])
        self.assertEqual(
            result.url_params,
            {} if not param['query_params'] else param['query_params'])
        self.assertEqual(result.http_method,
                         param['method'].upper())
