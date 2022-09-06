from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist, lev_dist_custom_dist, lev_dist_str
from chat.requests.check_out_request import RequestError
from chat.requests.request_factory import PresenceRequestCreator, CheckOutRequestCreator
import re


class CheckOutAdapter(CustomLogicAdapter):
    # Bot responses
    location_confirm_response = "Effettuare il check-out per la sede di "
    not_checked_in_response = "Non è possibile effettuare il checkout perché non risulti presente in alcuna sede."
    success_response = "Check-out effettuato correttamente per la sede di "
    exit_response = "Check-out annullato"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.sede = None

    def can_process(self, statement):
        check_out_words = ['check-out', 'checkout', 'lasciare', 'andare']

        # Sostituzione delle parole 'check out' con la parola 'check-out'
        cw = lev_dist_str(statement.text.split(), ['check'])
        if cw is not None:
            sub_str = cw + " out"
            statement.text = re.sub(sub_str, 'check-out', statement.text)

        words = statement.text.split()

        if self.processing_stage is not None:
            return True
        if lev_dist(words, check_out_words):
            self.processing_stage = "check-out"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'check-out' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Check-out processing stages
            if self.processing_stage == "check-out":
                if self.api_key is None:
                    self.processing_stage = None
                    response = Statement(self.not_login_response)
                    response.confidence = 1
                    return response
                else:
                    if self.check_presence():
                        self.processing_stage = "check-out confirm"
                        response_text = self.location_confirm_response + self.sede + "?"
                    else:
                        response_text = self.not_checked_in_response
                        self.processing_stage = None
                    confidence = 0.5
            elif self.processing_stage == "check-out confirm":
                yes_words = ["sì", "si", "ok", "yes", "s", "y", "vai"]
                no_words = ["no", "n", "nope"]
                if lev_dist_custom_dist(statement.text.split(), yes_words, 0):
                    request = CheckOutRequestCreator().get_request(self.api_key)
                    request.add_property("sede", str(self.sede))
                    request.send()
                    if request.get_status() == "Ok":
                        response_text = self.success_response + self.sede
                    else:
                        response_text = self.internal_error_response
                    self.processing_stage = None
                elif lev_dist_custom_dist(statement.text.split(), no_words, 0):
                    response_text = self.exit_response
                    self.processing_stage = None
                else:
                    response_text = self.incorrect_response + "\n" + self.location_confirm_response + \
                                    self.sede + "?"
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
        # Test Api Key: '87654321-4321-4321-4321-210987654321'
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
