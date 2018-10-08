# Introduce 
[![Build Status](https://travis-ci.org/TommyLike/huaweicloud-python-sdk-core.svg?branch=master)](https://travis-ci.org/TommyLike/huaweicloud-python-sdk-core)

This is the base library for HuaweiCloud python SDK, it provides the
basic logic to authorize, locate endpoint and perform low level API
requests, it's not for any standalone usage.

# Install

Install via pip:

```shell
    $ pip install huaweicloud-python-sdk-core
```

Install via github source code.

```shell
    $ git clone https://github.com/TommyLike/huaweicloud-python-sdk-core.git
    $ cd huaweicloud-python-sdk-core
    $ python setup.py install
```

**NOTE**: For Mac and python 3+ user, please install `requests[security]` as well,
[Reference](https://github.com/requests/requests/issues/3189).

# Tests

Use tox to run all test tasks.
```shell
tox
```
Functional testcases depend environment variables, therefore they are disabled
in default, in order to re-open them, please configure these at least:

```shell
export access_key_id=<access-key>
export access_key_secret=<secret-key>
export username=<username>
export password=<password>
export domain=<domain_name>
export auth_url=<auth_url>
export region=<region_id>
```


# Usage

These code below demonstrates how to use our client to invoke
EVS's [ListVolumes](https://support.huaweicloud.com/api-evs/zh-cn_topic_0058762430.html)
interface by inheriting
our basic ``BaseRequest`` object.  
**NOTE**: Please visit our [Official Endpoints](https://developer.huaweicloud.com/endpoint)
to get the ``region`` and ``auth_url`` information, for
more samples, please check [evs_sample.py](samples/evs_sample.py)

## Define service API specific Request
```python
import httplib

from huaweipythonsdkcore import request


class ListVolumesRequest(request.BaseRequest):

    _service = 'evs'

    _base_endpoint = '/volumes'

    _http_method = 'GET'

    _user_agent = 'huawei-python-sdk/1.0.1'
```
## Initialize client
We both support AK/SK and username/password credentials currently, use
```python

demo_client = client.Client(
    auth_url=<iam-endpoint-url> # for example, 'https://iam.cn-north-1.myhwclouds.com:443/v3',
    credential=credential.AccessKeyCredential(
        access_key_id=<access_key>,
        access_key_secret=<access_secret>
    ),
    region=<region-id>)
```
or
```python

 demo_client = client.Client(
         auth_url='https://iam.cn-north-1.myhwclouds.com:443/v3',
         credential=credential.PasswordCredential(
             username=<username>,
             password=<password>,
             domain=<domain>,
             project=<project> #in most of the cases it's equal to region
         ),
        region=<region-id>)
```
## Use client to invoke API via Request instance
```python

# Query available volumes
demo_client.handle_request(req=ListVolumesRequest())
```

## Use client to invoke API via raw request parameters
if you prefer a more simple and direct approach, you can invoke API
without constructing a `request` object.
```python
# Query available servers
demo_client = client.handle_raw_request(
    "nova", "GET", "/servers"):
```

## Wrap content with Response Object
Client only returns the raw API content in the format of tuple:

    (int_respond_code, string_respond_content, dict_respond_header)

It's better to deserialize them into Response object for better endpoint usage experience.

