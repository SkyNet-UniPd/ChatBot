from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist_custom_dist, lev_dist_str


class HelpAdapter(LogicAdapter):
    help_commands = ["login: permette di fare il login al sistema con la propria API Key",
                     "check-in: permette di effettuare la registrazione in una sede",
                     "check-out: permette di registrare il termine della propria presenza in una sede",
                     "consuntivare attività: permette di consuntivare una nuova attività per un progetto",
                     "ore consuntivate: permette di ottenere la consuntivazione totale delle ore di lavoro svolte per un progetto",
                     "stato presenza: permette di vedere lo stato di registrazione della presenza",
                     "logout: permette di effettuare il logout dal sistema"]

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement, additional_response_selection_parameters=None):
        help_words = ["aiuto", "help", "aiutami", "istruzioni"]

        input_words = statement.text.split()

        if lev_dist_custom_dist(input_words, help_words, 1):
            self.processing_stage = "help"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        response = Statement(
            "<strong>ℹ️ Help - Aiuto</strong><br/> Questa è la lista di tutti comandi disponbili offerti da "
            "SkyNetChatbot:<br/> " + self.ulify(self.help_commands))
        response.confidence = 1
        return response

    def ulify(self, elements):
        string = "<ul>\n"
        for s in elements:
            string += "<li>" + str(s) + "</li>\n"
        string += "</ul>"
        return string
