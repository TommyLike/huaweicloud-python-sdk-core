import httplib

from huaweipythonsdkcore import request


class EvsRequest(request.BaseRequest):

    _service = 'evs'

    _user_agent = 'huawei-python-sdk/1.0.1'


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

