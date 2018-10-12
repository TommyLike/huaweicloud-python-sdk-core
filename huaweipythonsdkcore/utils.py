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

import datetime

import six
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import urlencode
from six.moves.urllib import parse
from huaweipythonsdkcore import request
from huaweipythonsdkcore import exception

TIME_FORMAT = "%Y%m%dT%H%M%SZ"


def get_host_name(url):
    return parse.urlparse(url).hostname


def get_format_datetime():
    return datetime.datetime.strftime(datetime.datetime.utcnow(),
                                      TIME_FORMAT)


def get_url_path(url):
    return parse.urlparse(url).path


def get_request_endpoint(req, base_url):
    return "{}/{}".format(base_url.rstrip('/'), req.endpoint.lstrip('/'))


def collect_complete_headers(endpoint, request):
    h = request.headers.copy()
    for (key, value) in [('Content-Type', request.content_type),
                         ('Accept', request.accept),
                         ('User-Agent', request.user_agent)]:

        if key not in request.headers and value is not None:
            h[key] = value
    for (key, value) in [('Host', get_host_name(endpoint)),
                         ('X-Sdk-Date', get_format_datetime())]:
        h[key] = value
    return h


def build_request_object(service, method, path, headers=None,
                         query_params=None, body=None, timeout=None):
    if not service:
        raise exception.ValueException(
            "Service: {} should not be empty. ".format(service))
    if method is None or method.upper() not in ['GET', 'HEAD',
                                                'DELETE', 'POST',
                                                'PUT', 'PATCH', 'OPTIONS']:
        raise exception.ValueException(
            "Http method: {} is not supported now.".format(method))
    if timeout is not None and not isinstance(timeout, int):
        raise exception.ValueException(
            "Timeout only support integer now.")
    return request.BaseRequest(headers=headers, body=body,
                               url_params=query_params,
                               service=service,
                               method=method.upper(),
                               endpoint=path,
                               timeout=timeout)


def encode_parameters(paramters):
    if six.PY2:
        result = urlencode(paramters)
        # NOTE: Since python 2 doesn't support quota_via parameter
        # we hard code the special characters here.
        result = result.replace("+", "%20")
    else:
        result = urlencode(paramters, quota_via=quote)
    return result
