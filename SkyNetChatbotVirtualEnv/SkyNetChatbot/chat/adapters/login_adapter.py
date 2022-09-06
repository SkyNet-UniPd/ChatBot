from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist_custom_dist
from chat.requests.abstract_request import RequestError
from chat.requests.request_factory import AuthRequestCreator


class LoginAdapter(CustomLogicAdapter):
    # Bot responses
    login_response = "Inserisci la tua API Key."
    wrong_api_response = "L'API Key inserita non è corretta!"
    already_login_response = "Hai già effettuato il login!"
    success_response = "Login effettuato correttamente!"
    exit_response = "Login annullato."

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        login_words = ['login', 'accesso', 'autenticazione','log-in']

        if self.processing_stage is not None:
            return True

        if not lev_dist_custom_dist(statement.text.split(), login_words, 0):
            return False
        else:
            self.processing_stage = "login" 
            return True

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'login' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Login processing stages
            if self.processing_stage == "login":
                # Check if user is already logged in
                if self.api_key is not None: #Test API key:  "87654321-4321-4321-4321-210987654321"
                    response_text = self.already_login_response
                    self.processing_stage = None
                    response = Statement(response_text)
                    response.confidence = 0.5
                    return response
                else:
                    response_text = self.login_response
                    confidence = 0.5
                    self.processing_stage = "get api key"
            elif self.processing_stage == "get api key":
                # Check if the input is a valid API Key
                if self.check_api_key(statement.text):
                    response_text = self.success_response
                else:
                    response_text = self.wrong_api_response
                self.processing_stage = None
                confidence = 1
            else:
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

    def check_api_key(self, text: str):
        request = AuthRequestCreator().get_request(text)
        request.send()
        if request.get_status() == "Ok":
            return True
        elif request.get_status() == "NotFound":
            return False
        else:
            raise RequestError("InternalError")
