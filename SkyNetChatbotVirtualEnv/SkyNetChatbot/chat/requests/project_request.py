import requests
from chat.requests.abstract_request import AbstractRequest, RequestError


class ProjectRequest(AbstractRequest):

    def __init__(self, api_key):
        super().__init__(api_key)

    def send(self):
        url = 'https://apibot4me.imolinfo.it/v1/projects/'
        try:
            service_response = requests.get(url, headers={"api_key": self.api_key}, timeout=10)
        except requests.RequestException as req:
            raise RequestError(str(req.__class__.__name__)) from req
        if service_response.status_code == 200:
            self.status = "Ok"
        else:
            raise RequestError(str(service_response.status_code))
        return service_response
