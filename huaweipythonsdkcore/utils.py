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
import retrying
import random
import six
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


TIME_FORMAT = "%Y%m%dT%H%M%SZ"


def get_host_name(url):
    return urlparse(url).hostname


def get_format_datetime():
    return datetime.datetime.strftime(datetime.datetime.utcnow(),
                                      TIME_FORMAT)


def get_url_path(url):
    return urlparse(url).path


def get_request_endpoint(req, base_url):
    return "{}/{}".format(base_url.rstrip('/'), req.endpoint.lstrip('/'))


def collect_complete_headers(endpoint, request):
    h = request.headers.copy()
    for (key, value) in [('Content-Type', request.content_type),
                         ('Accept', request.accept),
                         ('User-Agent', request.user_agent),
                         ('Host', get_host_name(endpoint)),
                         ('X-Sdk-Date', get_format_datetime())]:

        if key not in request.headers and value is not None:
            h[key] = value
    return h


def retry(exceptions, interval=1, retries=3, backoff_rate=2,
          wait_random=False):

    def _retry_on_exception(e):
        return isinstance(e, exceptions)

    def _backoff_sleep(previous_attempt_number, delay_since_first_attempt_ms):
        exp = backoff_rate ** previous_attempt_number
        wait_for = interval * exp

        if wait_random:
            random.seed()
            wait_val = random.randrange(interval * 1000.0, wait_for * 1000.0)
        else:
            wait_val = wait_for * 1000.0

        # "Sleeping for %s seconds" % (wait_val / 1000.0)

        return wait_val

    def _print_stop(previous_attempt_number, delay_since_first_attempt_ms):
        delay_since_first_attempt = delay_since_first_attempt_ms / 1000.0
        # "Failed attempt %s" % previous_attempt_number
        # "Have been at this for %s seconds" % delay_since_first_attempt
        return previous_attempt_number == retries

    if retries < 1:
        raise ValueError('Retries must be greater than or '
                         'equal to 1 (received: %s). ' % retries)

    def _decorator(f):

        @six.wraps(f)
        def _wrapper(*args, **kwargs):
            r = retrying.Retrying(retry_on_exception=_retry_on_exception,
                                  wait_func=_backoff_sleep,
                                  stop_func=_print_stop)
            return r.call(f, *args, **kwargs)

        return _wrapper

    return _decorator