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

from huaweipythonsdkcore import credential
from huaweipythonsdkcore.sign import aksk_signer


def get_signer(cred, region):
    if isinstance(cred, credential.AccessKeyCredential):
        return aksk_signer.AKSKSigner(access_key=cred.access_key_id,
                                      secret_key=cred.access_key_secret,
                                      region=region)
    else:
        raise Exception("Unrecognized credential type: %s." % cred.__class__)
