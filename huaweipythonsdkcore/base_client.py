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

import httplib

import requests
from huaweipythonsdkcore import exception
from huaweipythonsdkcore import request_handler
from huaweipythonsdkcore import utils


class BaseClient(object):

    def __init__(self, authenticator=None):
        self.authenticator = authenticator
        self.handler = request_handler.RequestHandler.get_instance()

    def _do_request(self, req, full_path):

        def send(req, full_path, auth_method):
            headers = utils.collect_complete_headers(full_path, req)
            headers = auth_method(full_path, req.http_method, headers,
                                  body=req.body,
                                  params=req.url_params,
                                  service=req.service)
            return self.handler.handle_request(
                path=full_path,
                method=req.http_method,
                headers=headers,
                url_params=req.url_params,
                body=req.body,
                timeout=req.timeout,
                expected_code=req.success_code)
        try:
            result = send(req, full_path, self.authenticator.auth)
            if not (result[0] == httplib.UNAUTHORIZED and
                    self.authenticator.support_re_auth):
                return result
        except requests.exceptions.RequestException as err:
            raise exception.RequestException(err.message)
        except exception.HttpResponseException as e:
            if not (e.code == httplib.UNAUTHORIZED and
                    self.authenticator.support_re_auth):
                raise e
        # Re-auth and process request again
        try:
            return send(req, full_path, self.authenticator.re_auth)
        except requests.exceptions.RequestException as err:
            raise exception.RequestException(err.message)
