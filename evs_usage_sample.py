import time
import json
import os

from huaweipythonsdkcore import client
from huaweipythonsdkcore import credential
import evs_sdk_sample


# Initialize client

demo_client = client.Client(
    auth_url='https://iam.cn-north-1.myhwclouds.com:443/v3',
    credential=credential.AccessKeyCredential(
        access_key_id=os.environ['access_key_id'],
        access_key_secret=os.environ['access_key_secret']
    ),
    region='cn-north-1')

# Create a volume
create_volume = evs_sdk_sample.CreateVolumeRequest(
    name="this is created from huawei sdk core",
    description="this is the description",
    size=2,
    volume_type="SATA"
)

create_volume.Name = "this is the new name."

volume = demo_client.handle_request(req=create_volume)

print(volume)

volume_obj = json.loads(volume)

# Show volume detail
while volume_obj['volume']['status'] != 'available':
    volume = demo_client.handle_request(req=evs_sdk_sample.ShowVolumeRequest(
        volume_obj['volume']['id']))
    print(volume)
    time.sleep(1)
    volume_obj = json.loads(volume)

# Delete volume
print(demo_client.handle_request(req=evs_sdk_sample.DeleteVolumeRequest(
    volume_obj['volume']['id'])))

