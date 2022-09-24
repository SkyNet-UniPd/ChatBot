from chatterbot.conversation import Statement
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chat.lev_dist import lev_dist
from chat.requests.presence_request import RequestError
from chat.requests.request_factory import PresenceRequestCreator


class PresenceAdapter(CustomLogicAdapter):
    # Bot responses
    present_response = "Risulti presente nella sede di "
    not_present_response = "Non risulti presente in alcuna sede."
    exit_response = "Richiesta di tracciamento della presenza annullata"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.sede = None

    def can_process(self, statement):
        presence_words = ['stato', 'presenza', 'tracciamento']

        input_words = statement.text.split()

        if self.processing_stage is not None:
            return True
        if not lev_dist(input_words, presence_words):
            return False
        self.processing_stage = "presenza"
        return True

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'presenza' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Presence processing stages
            if self.processing_stage == "presenza":
                # Check if user is logged in
                if self.api_key is None:
                    self.processing_stage = None
                    response = Statement(self.not_login_response)
                    response.confidence = 1
                    return response
                else:
                    # Test API key: '87654321-4321-4321-4321-210987654321'
                    if self.check_presence():
                        response_text = self.present_response + self.sede + '.'
                    else:
                        response_text = self.not_present_response
                    self.processing_stage = None
                    confidence = 0.4
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
