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
from huaweipythonsdkcore.auth import aksk_authenticator
from huaweipythonsdkcore.auth import pwd_authenticator


def get_authenticator(cred, region, auth_url):

    if isinstance(cred, credential.AccessKeyCredential):
        return aksk_authenticator.AKSKAuthenticator(
            access_key=cred.access_key_id,
            secret_key=cred.access_key_secret,
            region=region)
    elif isinstance(cred, credential.PasswordCredential):
        return pwd_authenticator.PwdAuthenticator(username=cred.username,
                                                  password=cred.password,
                                                  domain=cred.domain,
                                                  project=cred.project,
                                                  auth_url=auth_url)

    else:
        raise Exception("Unrecognized credential type: %s." % cred.__class__)
