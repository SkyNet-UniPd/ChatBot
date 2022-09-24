import datetime
import requests
from chat.requests.abstract_request import AbstractRequest, RequestError


class ActivityRequest(AbstractRequest):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.project = None
        self.billableHours = None
        self.location = None
        self.notes = None
        self.date = datetime.date.today().strftime('%Y-%m-%d')

    def send(self):
        if self.properties.get("method") == "POST":
            self.project = self.properties.get("project")
            self.billableHours = self.properties.get("billableHours")
            self.location = self.properties.get("sede")
            self.notes = self.properties.get("notes")
            json_data = {
                "date": datetime.date.today().strftime('%Y-%m-%d'),
                "billableHours": self.billableHours,
                "travelHours": 0,
                "billableTravelHours": 0,
                "location": self.location,
                "billable": True,
                "note": self.notes
            }
            if self.is_ready():
                url = "https://apibot4me.imolinfo.it/v1/projects/" + self.project + "/activities/me"
                try:
                    service_response = requests.post(url, headers={"api_key": self.api_key,
                                                     "Content-Type": "application/json"},
                                                     json=[json_data], timeout=10)
                except requests.RequestException as req:
                    raise RequestError(str(req.__class__.__name__)) from req
                if service_response.status_code == 204:
                    self.status = "Ok"
                    return service_response
                else:
                    raise RequestError(str(service_response.status_code))
            else:
                raise RequestError(str("RequestNotReady"))
        else:  # Di default uso sempre GET
            if self.properties.get("dateFilter") and self.properties.get("project"):  # GET con filtro sulla data
                self.project = self.properties.get("project")
                data_filter = "from=" + str(self.date) + "&to=" + str(self.date)
                url = 'https://apibot4me.imolinfo.it/v1/projects/' + self.project + "/activities/me?" + data_filter
                try:
                    service_response = requests.get(url, headers={'api_key': self.api_key}, timeout=10)
                except requests.RequestException as req:
                    raise RequestError(str(req.__class__.__name__)) from req
                if service_response.status_code == 200 and service_response.content:
                    self.status = "Ok"
                else:
                    raise RequestError(str(service_response.status_code))
                return service_response
            else:
                raise RequestError()

    def is_ready(self):
        if self.properties.get("project") and self.properties.get("billableHours") and self.properties.get("sede"):
            return True
        return False

    
