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


import sys

import six


def get_utf8_bytes(message):
    """Get the bytes array encoded by utf-8.

    :param message: the string of message
    :type message: string
    """
    if six.PY2:
        message = message.decode(
            sys.stdin.encoding if sys.stdin.encoding else 'cp936')
    return message.encode('utf8')
