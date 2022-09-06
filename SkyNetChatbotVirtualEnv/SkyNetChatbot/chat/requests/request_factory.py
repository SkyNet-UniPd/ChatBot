from chat.requests.abstract_request import AbstractRequest, RequestError
from chat.requests.check_in_request import CheckInRequest
from chat.requests.check_out_request import CheckOutRequest
from chat.requests.presence_request import PresenceRequest
from chat.requests.location_request import LocationRequest
from chat.requests.project_request import ProjectRequest
from chat.requests.activity_request import ActivityRequest
from chat.requests.auth_request import AuthRequest


class AbstractRequestFactory:

    def __init__(self):
        pass

    def get_request(self, api_key=None) -> AbstractRequest:
        return self.create_request(api_key)

    def create_request(self, api_key):
        raise RequestError("RequestNotImplemented")


class CheckInRequestCreator(AbstractRequestFactory):

    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> CheckInRequest:
        return CheckInRequest(api_key)


class PresenceRequestCreator(AbstractRequestFactory):

    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> PresenceRequest:
        return PresenceRequest(api_key)


class CheckOutRequestCreator(AbstractRequestFactory):

    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> CheckOutRequest:
        return CheckOutRequest(api_key)


class LocationRequestCreator(AbstractRequestFactory):

    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> LocationRequest:
        return LocationRequest(api_key)


class ProjectRequestCreator(AbstractRequestFactory):
    
    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> ProjectRequest:
        return ProjectRequest(api_key)


class ActivityRequestCreator(AbstractRequestFactory):
    
    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> ActivityRequest:
        return ActivityRequest(api_key)


class AuthRequestCreator(AbstractRequestFactory):
    
    def __init__(self):
        super().__init__()

    def create_request(self, api_key) -> AuthRequest:
        return AuthRequest(api_key)
