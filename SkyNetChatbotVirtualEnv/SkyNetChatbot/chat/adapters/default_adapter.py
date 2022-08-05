from chatterbot.conversation import Statement
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chat.lev_dist import lev_dist
import re


class DefaultAdapter(CustomLogicAdapter):

    defaultMessageIT = "Mi spiace, ma non riesco ad interpretare la tua richiesta! :("
    helloResponse = "Ciao, sono SkyNetChatbot, un bot che ti aiuta a gestire il tuo lavoro.\n" \
                    "Chiedimi qualcosa e io cercherò di risponderti nel migliore dei modi.\n" \
                    "Per esempio, per effettuare il check-in dimmi semplicemente: 'check-in'.\n" \
                    "Al momento sono disponibili solo le funzioni di check-in e check-out!"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        hello_words = ["ciao", "hey", "buongiorno", "buonasera"]
        help_words = ["aiuto", "help", "aiutami", "istruzioni"]  # Momentaneo, poi l'help avrà un suo logic adapter

        input_words = re.sub(r"[^a-zA-Z0-9 \n.\-/]", ' ', statement.text).split()

        if lev_dist(input_words, hello_words) or lev_dist(input_words, help_words):
            response_text = self.helloResponse
            confidence = 0.3
        else:
            response_text = self.defaultMessageIT
            confidence = 0.1

        response = Statement(response_text)
        response.confidence = confidence
        return response
