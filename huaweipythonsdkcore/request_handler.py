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

from huaweipythonsdkcore import exception
from huaweipythonsdkcore import utils


class RequestHandler(object):

    _Instance = None

    def __init__(self):
        self._session = requests.Session()

    @classmethod
    def get_instance(cls):
        if RequestHandler._Instance is None:
            RequestHandler._Instance = RequestHandler()
        return RequestHandler._Instance

    @utils.retry(requests.exceptions.Timeout, retries=3, backoff_rate=2)
    def handle_request(self, path, method, headers, url_params, body,
                       timeout=None, expected_code=None):
        http_method = getattr(self._session, method.lower(), None)
        if http_method is None:
            raise Exception("Unable to find http "
                            "method: %s." % method.lower())
        parameters = {
            'headers': headers
        }
        if timeout:
            parameters['timeout'] = timeout
        if body:
            parameters['json'] = body
        if url_params:
            parameters['params'] = url_params

        response = http_method(path, **parameters)
        if isinstance(expected_code, list):
            if response.status_code not in expected_code:
                raise exception.HttpResponseException(
                    response.text, response.status_code,
                    ','.join(map(str, expected_code)))
        elif isinstance(expected_code, int):
            if response.status_code != expected_code:
                raise exception.HttpResponseException(
                    response.text, response.status_code, expected_code)
        return response.status_code, response.text
