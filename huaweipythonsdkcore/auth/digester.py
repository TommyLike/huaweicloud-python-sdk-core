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

import hashlib
import hmac


class Sha256(object):

    @property
    def algorithm_name(self):
        return "SDK-HMAC-SHA256"

    def get_digest(self, key, message):
        return hmac.new(key, message,
                        digestmod=hashlib.sha256).digest()

    def get_hex_digest(self, key, message):
        return hmac.new(key, message,
                        digestmod=hashlib.sha256).hexdigest()
