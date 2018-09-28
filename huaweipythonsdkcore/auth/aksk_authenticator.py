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
import json
import urllib

import six
from huaweipythonsdkcore.auth.authenticator import Authenticator
from huaweipythonsdkcore.auth import digester
from huaweipythonsdkcore.auth import utils as sign_util
from huaweipythonsdkcore import utils

TERMINATORSTRING = "sdk_request"


class AKSKAuthenticator(Authenticator):

    SIGN_HEADER = 'Authorization'
    _re_auth = False

    def __init__(self, access_key=None, secret_key=None, region=None):
        self.ak = access_key
        self.sk = secret_key
        self.region = region
        self.headtosign = ['Host', 'X-Sdk-Date']
        self.digester = digester.Sha256()

    def _make_canonical_request(self, method=None, url=None, headers=None,
                                params=None, body=None):
        """
        Create a canonical request string
        :param method : the request's http method, get/post OR other
        :type method : string
        :param url : the full path url
        :type url : string
        :param headers : the http request header,must contains Host and
        X-Sdk-Date fields
        :type headers : python dict
        :param params : the http request query parameters
        :type params : python dict
        :param body : the http request body
        :type body : python dict
        :return: A string of canonical request
        """
        canonical_method = method.upper() if method else ''
        body = body if body else ''
        if isinstance(body, dict):
            body = json.dumps(body)
        uri = utils.get_url_path(url)
        uri = uri.replace(":", "%3A")
        canonical_uri = uri if uri.endswith('/') else uri + '/'
        if params:
            result = []
            for k, vs in list(params.items()):
                if (isinstance(vs, six.string_types) or
                        not hasattr(vs, '__iter__')):
                    vs = [vs]
                for v in vs:
                    if v is not None:
                        result.append(
                            (k.encode('utf-8') if isinstance(k, str) else k,
                             v.encode('utf-8') if isinstance(v, str) else v))
            result.sort(key=lambda item: item[0])
            canonical_querystring = urllib.urlencode(result, doseq=True)
        else:
            canonical_querystring = ''
        canonical_header = [
            k.lower() + ':' + headers.get(k).strip() for
            k in self.headtosign] if all(
            [k in headers for k in self.headtosign]) else []
        canonical_header = '\n'.join(canonical_header)
        canonical_header += '\n'
        signed_header = ';'.join([k.lower() for k in self.headtosign])

        request_payload = hashlib.sha256(body).hexdigest()
        return '\n'.join([canonical_method, canonical_uri,
                          canonical_querystring, canonical_header,
                          signed_header, request_payload])

    def _make_string_to_sign(self, canonical_req, dtstamp, svr):
        request_datetime = dtstamp
        request_date = dtstamp.split('T')[0]
        credential_scope = '/'.join(
            [request_date, self.region, svr, TERMINATORSTRING])
        hashed_request = hashlib.sha256(
            sign_util.get_utf8_bytes(canonical_req)).hexdigest()
        return "\n".join([self.digester.algorithm_name, request_datetime,
                          credential_scope, hashed_request]), credential_scope

    def _make_signing_key(self, dtstamp, svr):
        """
        :param dtstamp: datetime stamp of UTC
        :type dtstamp : string
        :param svr: the name of service defined in  sdk
        :type svr :string
        :return: A string to be used as the key when encry the request string
        """
        ksecret = "SDK" + self.sk
        kdate = self.digester.get_digest(
            sign_util.get_utf8_bytes(ksecret),
            sign_util.get_utf8_bytes(dtstamp[0:8]))
        kregion = self.digester.get_digest(
            kdate,
            sign_util.get_utf8_bytes(self.region))
        kservice = self.digester.get_digest(
            kregion,
            sign_util.get_utf8_bytes(svr))
        return self.digester.get_digest(
            kservice, sign_util.get_utf8_bytes(TERMINATORSTRING))

    def auth(self, url=None, method=None, headers=None, body=None, params=None,
             service=None):
        canonical_request = self._make_canonical_request(method=method,
                                                         url=url,
                                                         params=params,
                                                         headers=headers,
                                                         body=body)
        # print canonical_request
        signing_key = self._make_signing_key(headers.get("X-Sdk-Date"),
                                             service)
        string_to_sign, credential_scope = self._make_string_to_sign(
            canonical_request, headers.get("X-Sdk-Date"), service)
        signature = self.digester.get_hex_digest(
            signing_key,
            sign_util.get_utf8_bytes(string_to_sign))
        signed_header = ';'.join([k.lower() for k in self.headtosign])

        headers[self.SIGN_HEADER] = "%s Credential=%s/%s, SignedHeaders=%s, " \
                                    "Signature=%s" % (
            self.digester.algorithm_name, self.ak, credential_scope,
            signed_header, signature)
        return headers
