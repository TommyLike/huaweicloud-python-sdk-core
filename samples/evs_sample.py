import httplib
import os
import json
import time

from huaweipythonsdkcore import request
from huaweipythonsdkcore import credential
from huaweipythonsdkcore import client
from huaweipythonsdkcore import exception


class EvsRequest(request.BaseRequest):

    _service = 'evs'

    _user_agent = 'huawei-python-sdk/0.0.1'


class CreateVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes'

    _http_method = 'POST'

    _success_codes = [httplib.CREATED, httplib.ACCEPTED]

    _available_attributes = {
        'Name': str,
        'Description': str,
        'Size': int,
        'Volume_Type': str
    }

    def __init__(self, name, description, size, volume_type):
        body = {'volume': {'name': name,
                           'description': description,
                           'size': size,
                           'volume_type': volume_type}}
        super(CreateVolumeRequest, self).__init__(body=body)

    def __getattr__(self, item):
        if item in self._available_attributes:
            return self.body['volume'][item.lower()]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self._available_attributes:
            if not isinstance(value, self._available_attributes[key]):
                raise ValueError("{} should be an instance of {}".format(
                    key, self._available_attributes[key]))
            self.body['volume'][key.lower()] = value
        else:
            super(CreateVolumeRequest, self).__setattr__(key, value)


class ShowVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'GET'

    _success_codes = [httplib.OK]

    def __init__(self, volume_id):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        super(ShowVolumeRequest, self).__init__()


class UpdateVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'PUT'

    _success_codes = [httplib.OK]

    def __init__(self, volume_id):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        super(UpdateVolumeRequest, self).__init__()


class DeleteVolumeRequest(EvsRequest):

    _base_endpoint = '/volumes/{volume_id}'

    _http_method = 'DELETE'

    def __init__(self, volume_id):
        self._base_endpoint = self._base_endpoint.replace("{volume_id}",
                                                          volume_id)
        super(DeleteVolumeRequest, self).__init__()


if __name__ == "__main__":

    # Initialize the client
    demo_client = client.Client(
        auth_url='https://iam.cn-north-1.myhwclouds.com:443/v3',
        credential=credential.AccessKeyCredential(
            access_key_id=os.environ['access_key_id'],
            access_key_secret=os.environ['access_key_secret']
        ),
        region='cn-north-1')

    try:
        # Create a volume
        create_volume = CreateVolumeRequest(
            name="this is created from huawei sdk core",
            description="this is the description",
            size=2,
            volume_type="SATA"
        )

        create_volume.Name = "this is the updated name."
        create_volume.Description = "this is the updated description."

        code, volume = demo_client.handle_request(req=create_volume)

        print(volume)

        volume_obj = json.loads(volume)

        # Show volume detail
        while volume_obj['volume']['status'] != 'available':
            code, volume = demo_client.handle_request(req=ShowVolumeRequest(
                volume_obj['volume']['id']))
            print(volume)
            time.sleep(1)
            volume_obj = json.loads(volume)

        # Delete volume
        print(demo_client.handle_request(req=DeleteVolumeRequest(
            volume_obj['volume']['id'])))
    except exception.SDKException as err:
        print(err)

