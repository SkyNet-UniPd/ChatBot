from chatterbot.conversation import Statement
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chat.lev_dist import lev_dist_custom_dist


class LogoutAdapter(CustomLogicAdapter):
    no_logged_user_response = "Non è possibile eseguire il logout perché non risulta fatto alcun accesso!"
    logout_confirm_response = "Confermi di voler effettuare il logout?"
    success_response = "Logout eseguito correttamente!"
    exit_response = "Logout annullato"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        logout_words = ['logout', 'log-out', 'esci', 'exit', 'uscire']

        if self.processing_stage is not None:
            return True

        if lev_dist_custom_dist(statement.text.split(), logout_words, 0):
            self.processing_stage = "logout"
            return True
        return False

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'logout' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        # Loogut processing stage
        if self.processing_stage == 'logout':
            # check if user is logged in
            if self.api_key is None:
                response_text = self.no_logged_user_response 
                self.processing_stage = None
                response = Statement(response_text)
                response.confidence = 0.5
                return response
            else:
                response_text = self.logout_confirm_response 
                confidence = 0.5
                self.processing_stage = "logout confirm"
        elif self.processing_stage == 'logout confirm':
            # Check confirmation logout
            yes_words = ["sì", "si", "ok", "yes", "s", "y", "vai"]
            no_words = ["no", "n", "nope"]
            if lev_dist_custom_dist(statement.text.split(), yes_words, 0):
                self.processing_stage = None
                response_text = self.success_response
            elif lev_dist_custom_dist(statement.text.split(), no_words, 0):
                response_text = self.exit_response
                self.processing_stage = None
            else:
                response_text = self.incorrect_response + "\n" + self.logout_confirm_response + "?"
            confidence = 1
        else:  # Non dovrebbe mai arrivare qui
            self.processing_stage = None
            response_text = self.internal_error_response
            confidence = 1

        response = Statement(response_text)
        response.confidence = confidence
        return response
