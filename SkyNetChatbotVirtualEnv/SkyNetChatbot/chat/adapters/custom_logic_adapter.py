from chatterbot.logic import LogicAdapter
from chat.lev_dist import lev_dist_custom_dist
import re


class CustomLogicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.processing_stage = None

    @staticmethod
    def check_exit(statement):
        input_words = re.sub(r"[^a-zA-Z0-9 \n.\-/]", ' ', statement.text).split()

        exit_words = ['esci', 'chiudi', 'annulla', 'stop', 'fine', 'exit']
        if lev_dist_custom_dist(input_words, exit_words, 1):
            return True
        else:
            return False
