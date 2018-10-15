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

import multiprocessing


class Configuration(object):

    def __init__(self, **kwargs):

        # ssl verification related options
        self.verify_ssl = kwargs[
            'verify_ssl'] if 'verify_ssl' in kwargs else False
        self.ca_certs = kwargs['ca_certs'] if 'ca_certs' in kwargs else []
        # Http retries
        self.retries = kwargs['retries'] if 'retries' in kwargs else 3
        # Connection timeout
        self.timeout = kwargs['timeout'] if 'timeout' in kwargs else 60
        # Http connection pool size
        self.pool_size = (kwargs['pool_size']
                          if 'pool_size' in kwargs
                          else multiprocessing.cpu_count() * 5)
