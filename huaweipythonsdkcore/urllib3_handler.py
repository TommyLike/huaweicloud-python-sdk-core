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

import json
import multiprocessing
import ssl

from huaweipythonsdkcore import exception
import six
from six.moves.urllib.parse import urlencode
import urllib3
from urllib3.util import retry


class RequestHandler(object):

    _Instance = None
    _Pool_Size = multiprocessing.cpu_count() * 5
    _Max_Retry = 3

    def __init__(self, ssl_verification=None):

        if ssl_verification is None:
            self.pool_manager = urllib3.PoolManager(
                num_pools=self._Pool_Size,
                cert_reqs=ssl.CERT_NONE,
                retries=retry.Retry(connect=self._Max_Retry))
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        else:
            raise exception.SDKException("SSL/TLS is not supported.")

    @classmethod
    def get_instance(cls, ssl_verification=None):
        if RequestHandler._Instance is None:
            RequestHandler._Instance = RequestHandler(ssl_verification)
        return RequestHandler._Instance

    def handle_request(self, path, method, headers, url_params, body,
                       timeout=None):
        method = method.upper()
        timeout = urllib3.Timeout(total=timeout)

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
            if body:
                if isinstance(body, dict):
                    body = json.dumps(body)
            if url_params:
                path += '?' + urlencode(url_params)
            result = self.pool_manager.request(
                method, path,
                body=body,
                preload_content=True,
                timeout=timeout,
                headers=headers)
        else:
            result = self.pool_manager.request(
                method, path,
                fields=url_params,
                preload_content=True,
                timeout=timeout,
                headers=headers)

        body = result.data
        # In the python 3, the response.data is bytes.
        # we need to decode it to string.
        if six.PY3:
            body = result.data.decode('utf8')

        return result.status, body, dict(result.headers)
