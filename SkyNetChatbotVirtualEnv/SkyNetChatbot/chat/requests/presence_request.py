import requests
from chat.requests.abstract_request import AbstractRequest, RequestError


class PresenceRequest(AbstractRequest):

    def __init__(self, api_key):
        super().__init__(api_key)

    def send(self):
        url = 'https://apibot4me.imolinfo.it/v1/locations/presence/me'
        try:
            service_response = requests.get(url, headers={'api_key': self.api_key})
        except requests.RequestException as req:
            raise RequestError(str(req.__class__.__name__))
        if service_response.status_code == 200:
            self.status = "Ok"
        elif service_response.status_code == 404:
            self.status = "NotFound"
        else:
            raise RequestError(str(service_response.status_code))
        return service_response
