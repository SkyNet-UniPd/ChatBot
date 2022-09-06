from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist, lev_dist_custom_dist, lev_dist_str, lev_dist_str_correct_w
from chat.requests.check_in_request import RequestError
import re
from chat.requests.request_factory import CheckInRequestCreator, PresenceRequestCreator, LocationRequestCreator


class CheckInAdapter(CustomLogicAdapter):
    # Bot responses
    wrong_sede_response = "La sede che hai inserito non esiste!"
    sede_response = "In quale sede vuoi effettuare il check-in?"
    checkin_done_response = "Hai già fatto il check-in nella sede di "
    success_response = "Check-in effettuato correttamente nella sede di "
    exit_response = "Check-in annullato"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.sede = None

    def can_process(self, statement, additional_response_selection_parameters=None):
        check_in_words = ['check-in', 'checkin', 'arrivato', 'entrato', 'entro']

        # Sostituzione delle parole 'check in' con la parola 'check-in'
        cw = lev_dist_str(statement.text.split(), ['check'])
        if cw is not None:
            sub_str = cw + " in"
            statement.text = re.sub(sub_str, 'check-in', statement.text)

        words = statement.text.split()

        if self.processing_stage is not None:
            return True

        if lev_dist_custom_dist(words, check_in_words, 1):
            self.processing_stage = "check-in"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'check-in' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Check-in processing stages
            if self.processing_stage == "check-in":
                if self.api_key is None:
                    self.processing_stage = None
                    response = Statement(self.not_login_response)
                    response.confidence = 1
                    return response
                else:
                    if not self.check_presence():
                        response_text = self.sede_response
                        self.processing_stage = "check-in sede"
                    else:
                        response_text = self.checkin_done_response + self.sede
                        self.processing_stage = None
                    confidence = 0.5
            elif self.processing_stage == "check-in sede":
                if self.check_sede(statement.text):
                    request = CheckInRequestCreator().get_request(self.api_key)
                    request.add_property("sede", str(self.sede))
                    request.send()
                    if request.get_status() == "Ok":
                        response_text = self.success_response + self.sede
                    else:
                        response_text = self.internal_error_response
                    self.processing_stage = None
                else:
                    response_text = self.wrong_sede_response + "\n" + self.sede_response
                confidence = 1
            else:  # Non dovrebbe mai arrivare qui
                self.processing_stage = None
                response_text = self.internal_error_response
                confidence = 1
        except RequestError as error:
            self.processing_stage = None
            response_text = error.__str__()
            confidence = 1

        response = Statement(response_text)
        response.confidence = confidence
        return response

    def check_presence(self):
        # Test APi key: '87654321-4321-4321-4321-210987654321'
        request = PresenceRequestCreator().get_request(self.api_key)
        request_response = request.send()
        # Check user presence
        if request.get_status() == "Ok":
            self.sede = str(request_response.json()['location'])
            return True
        elif request.get_status() == "NotFound":
            return False
        else:
            raise RequestError("InternalError")

    def check_sede(self, text: str):
        locations = []
        location_request = LocationRequestCreator().get_request(self.api_key)
        request_response = location_request.send()
        if location_request.get_status() == "Ok":
            for item in request_response.json():
                locations.append(item['name'])
        if lev_dist(text.split(), locations):
            self.sede = lev_dist_str_correct_w(text.split(), locations)
            return True
        else:
            return False

