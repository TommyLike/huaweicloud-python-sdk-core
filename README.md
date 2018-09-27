# Introduce

This is the base library for HuaweiCloud python SDK, it provides the
basic logic to authorize, locate endpoint and perform low level API
requests, it's not for any standalone usage, although we are working
in progress, any contribution is welcome.

# Usage

These code below demonstrates how to use our client to invoke
EVS's [ListVolumes](https://support.huaweicloud.com/api-evs/zh-cn_topic_0058762430.html)
interface by inheriting
our basic ``BaseRequest`` object.
**NOTE**: Please visit our [endpoint website](https://developer.huaweicloud.com/endpoint)
to get the ``region`` and ``auth_url`` information, for
more samples, please check [evs_sample.py](samples/evs_sample.py)

```python
import httplib

from huaweipythonsdkcore import request


class ListVolumesRequest(request.BaseRequest):

    _service = 'evs'

    _base_endpoint = '/volumes'

    _http_method = 'GET'

    _user_agent = 'huawei-python-sdk/1.0.1'


# Initialize client
demo_client = client.Client(
    auth_url=<iam-endpoint-list> # for example, 'https://iam.cn-north-1.myhwclouds.com:443/v3',
    credential=credential.AccessKeyCredential(
        access_key_id=<access_key>,
        access_key_secret=<access_secret>
    ),
    region=<region-id>)

# Query available volumes
demo_client.handle_request(req=ListVolumesRequest())

```
