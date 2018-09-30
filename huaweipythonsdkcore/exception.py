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


class SDKException(Exception):

    def __init__(self, code=None, message=None):
        self._code = code
        self._message = message

    def __str__(self):
        return "[SDKException] Message:%s Code:%s ." % (self.message,
                                                        self.code)

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


class EndpointResolveException(SDKException):

    def __init__(self, message):
        message = "Failed to resolve endpoint: {}".format(message)
        super(EndpointResolveException, self).__init__(code=None,
                                                       message=message)


class ValueException(SDKException):

    def __init__(self, message):
        message = "Unexpected parameters are specified: {}.".format(message)
        super(ValueException, self).__init__(code=None,
                                             message=message)


class RequestException(SDKException):

    def __init__(self, message):
        message = "Failed to proceed request to service " \
                  "endpoint, could be a low level error: {}.".format(message)
        super(RequestException, self).__init__(code=None,
                                               message=message)


class AuthException(SDKException):

    def __init__(self, message, credential):
        message = "Failed to authorize with provided " \
                  "information {}, message: {}.".format(credential, message)
        super(AuthException, self).__init__(code=None,
                                            message=message)
