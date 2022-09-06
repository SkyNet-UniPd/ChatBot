import requests
from chat.requests.abstract_request import AbstractRequest, RequestError


class CheckInRequest(AbstractRequest):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.sede = None

    def send(self):
        self.sede = self.properties.get("sede")
        if self.is_ready():
            url = 'https://apibot4me.imolinfo.it/v1/locations/' + self.sede + '/presence'
            try:
                service_response = requests.post(url, headers={"api_key": self.api_key,
                                                               "Content-Type": "application/json"})
            except requests.RequestException as req:
                raise RequestError(str(req.__class__.__name__))
            if service_response.status_code == 204:
                self.status = "Ok"
                return service_response
            else:
                raise RequestError(str(service_response.status_code))
        else:
            raise RequestError(str("RequestNotReady"))

    def is_ready(self):
        if self.sede is not None:
            return True
        else:
            return False
