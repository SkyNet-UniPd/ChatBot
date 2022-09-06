from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chat.lev_dist import lev_dist_custom_dist


class DefaultAdapter(LogicAdapter):

    default_message = "Mi spiace, ma non riesco ad interpretare la tua richiesta! 😔"
    hello_response = "👋 Ciao, sono SkyNetChatbot, un bot 🤖 che ti aiuta a gestire il tuo lavoro.<br/>" \
                     "Chiedimi qualcosa e io cercherò di risponderti nel migliore dei modi.<br/>" \
                     "Per esempio, per effettuare il Login dimmi semplicemente: 'login'.<br/>" \
                     "Per scoprire tutte le funzionalità dimmi 'help' o 'aiuto' per ottenere la lista dei comandi disponbili."

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):

        hello_words = ["ciao", "hey", "buongiorno", "buonasera"]
        input_words = statement.text.split()

        if lev_dist_custom_dist(input_words, hello_words, 1):
            response_text = self.hello_response
            confidence = 1
        else:
            response_text = self.default_message
            confidence = 0.1

        response = Statement(response_text)
        response.confidence = confidence
        return response
