from chatterbot.logic import LogicAdapter
from chat.lev_dist import lev_dist_custom_dist


class CustomLogicAdapter(LogicAdapter):
    # Bot responses for all adapters
    internal_error_response = "Ops, qualcosa è andato storto... Riprova ad effettuare l'operazione"
    incorrect_response = "Non ho capito la tua richiesta..."
    not_login_response = "Devi effettuare il login per completare l'operazione!"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.processing_stage = None
        self.api_key = None

    @staticmethod
    def check_exit(statement):
        input_words = statement.text.split()

        exit_words = ['chiudi', 'annulla', 'stop', 'fine', 'esci', 'exit']
        if lev_dist_custom_dist(input_words, exit_words, 1):
            return True
        return False

    def reset_processing_stage(self):
        self.processing_stage = None

    def is_processing_stage_none(self):
        return self.processing_stage is None

    def update_api_key(self, api_key):
        self.api_key = api_key

