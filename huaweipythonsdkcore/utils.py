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

from six.moves.urllib import parse

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
