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

from huaweipythonsdkcore.auth.authenticator import Authenticator
from huaweipythonsdkcore import urllib3_handler
from huaweipythonsdkcore import utils
from huaweipythonsdkcore import request


class AuthenticationRequest(request.BaseRequest):

    _service = 'identity'
    _base_endpoint = '/auth/tokens'
    _http_method = 'POST'
    _timeout = 60


class PwdAuthenticator(Authenticator):

    SIGN_HEADER = 'X-Auth-Token'
    AUTH_HEADER = 'X-Subject-Token'
    _re_auth = True

    def __init__(self, credential, auth_url=None, configuration=None):
        self.username = credential.username
        self.password = credential.password
        self.domain = credential.domain
        self.project = credential.project
        self.auth_url = auth_url
        self.handler = urllib3_handler.RequestHandler.get_instance(
            configuration=configuration)
        self._auth_token_cache = None

    @property
    def auth_content(self):
        return {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username,
                            'password': self.password,
                            'domain': {
                                'name': self.domain
                            }
                        }
                    }
                },
                'scope': {
                    'domain': {
                        'name': self.domain,
                    },
                    'project': {
                        'name': self.project
                    }
                }
            }
        }

    def _get_token(self):
        req = AuthenticationRequest()
        _, _, headers = self.handler.handle_request(
            path=utils.get_request_endpoint(req, self.auth_url),
            method=req.http_method,
            headers={},
            url_params=None,
            body=self.auth_content,
            timeout=req.timeout)
        return headers[self.AUTH_HEADER]

    def auth(self, url=None, method=None, headers=None, body=None, params=None,
             service=None):
        if self._auth_token_cache is None:
            self._auth_token_cache = self._get_token()
        hds = headers.copy()
        hds[self.SIGN_HEADER] = self._auth_token_cache
        return hds

    def re_auth(self, url=None, method=None, headers=None,
                body=None, params=None, service=None):
        self._auth_token_cache = None
        return self.auth(url=url, method=method, headers=headers,
                         body=body, params=method, service=service)
