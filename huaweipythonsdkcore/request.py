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


class BaseRequest(object):
    """Base request class.

    This class includes all required elements regarding HTTP request.
    """

    # Name of service that the request belongs to.
    _service = None
    # Request's relative endpoint, for example: '/server/{server_id}'
    _base_endpoint = '/'

    # Http method for this request, 'POST/GET/UPDATE/DELETE/....',
    # reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    _http_method = 'GET'

    # Request timeout of seconds.
    _timeout = 30

    # Request content type
    _content_type = 'application/json'

    # Accept type
    _accept = 'application/json'

    # User agent
    _user_agent = 'huaweicloud-python-sdk/0.0.1'

    # Type of endpoint
    _interface = 'public'

    def __init__(self,
                 headers=None,
                 url_params=None,
                 body=None):
        self._headers = {} if headers is None else headers
        self._url_params = {} if url_params is None else url_params
        self._body = {} if body is None else body
        if [item for item in [
                self._headers, self._url_params, self._body] if not isinstance(
                item, dict)]:
            raise ValueError(
                "'header', 'url_params' and 'body' should be dictionary.")
        self._host = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if not isinstance(value, dict):
            raise ValueError("'header' should be a dictionary.")
        self._headers = value

    @property
    def url_params(self):
        return self._url_params

    @url_params.setter
    def url_params(self, value):
        if not isinstance(value, dict):
            raise ValueError("'url' params should be a dictionary.")
        self._url_params = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if not isinstance(value, dict):
            raise ValueError("'body' should be a dictionary.")
        self._body = value

    @property
    def endpoint(self):
        return self._base_endpoint

    @property
    def content_type(self):
        return self._content_type

    @property
    def accept(self):
        return self._accept

    @property
    def user_agent(self):
        return self._user_agent

    @property
    def service(self):
        return self._service

    @property
    def http_method(self):
        return self._http_method

    @property
    def interface(self):
        return self._interface

    @property
    def timeout(self):
        return self._timeout
