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
import ssl

import certifi
import six
from huaweipythonsdkcore import utils
import urllib3
from urllib3.util import retry
from huaweipythonsdkcore import configuration as con
from huaweipythonsdkcore import exception


class RequestHandler(object):

    _Instance = None

    def __init__(self, configuration=None):

        if configuration is None:
            configuration = con.Configuration()
        if not isinstance(configuration, con.Configuration):
            raise exception.InvalidConfigException(
                "configuration object is not an instance of Configuration.")

        cert_reqs = ssl.CERT_NONE
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        if cert_reqs == ssl.CERT_NONE:
            self.pool_manager = urllib3.PoolManager(
                num_pools=configuration.pool_size,
                cert_reqs=cert_reqs,
                retries=retry.Retry(connect=configuration.retries),
                timeout=configuration.timeout)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        else:
            if configuration.ca_certs:
                ca_certs = configuration.ca_certs
            else:
                # if not set certificate file, use Mozilla's root certificates.
                ca_certs = certifi.where()
            self.pool_manager = urllib3.PoolManager(
                num_pools=configuration.pool_size,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                retries=retry.Retry(connect=configuration.retries),
                timeout=configuration.timeout)

    @classmethod
    def get_instance(cls, configuration=None):
        if RequestHandler._Instance is None:
            RequestHandler._Instance = RequestHandler(configuration)
        return RequestHandler._Instance

    def handle_request(self, path, method, headers, url_params, body,
                       timeout=None):
        method = method.upper()

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        if body:
            if isinstance(body, dict):
                body = json.dumps(body)
        if url_params:
            path += '?' + utils.encode_parameters(url_params)
        request_param = {
            'method': method,
            'url': path,
            'body': body,
            'preload_content': True,
            'headers': headers
        }
        if timeout is not None:
            request_param['timeout'] = timeout

        result = self.pool_manager.request(**request_param)

        body = result.data
        # In the python 3, the response.data is bytes.
        # we need to decode it to string.
        if six.PY3:
            body = result.data.decode('utf8')

        return result.status, body, dict(result.headers)
