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

from abc import ABCMeta, abstractmethod


class Credential(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        pass


class AccessKeyCredential(Credential):

    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def __str__(self):
        return "AccessKey: {}, KeySecret: {}".format(self.access_key_id,
                                                     self.access_key_secret)


class PasswordCredential(Credential):

    def __init__(self, username, password, domain, project):
        self.username = username
        self.password = password
        self.domain = domain
        self.project = project

    def __str__(self):
        return "Username: {}, Password: {}, Domain: {}, " \
               "Project: {}.".format(self.username,
                                     self.password,
                                     self.domain,
                                     self.project)
