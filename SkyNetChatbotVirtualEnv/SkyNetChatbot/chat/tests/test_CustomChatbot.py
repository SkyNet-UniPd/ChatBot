import requests
from django.test import TestCase
from chatterbot.conversation import Statement
from chat.custom_chatbot import CustomChatBot
from chat.adapters.default_adapter import DefaultAdapter
from chat.adapters.check_in_adapter import CheckInAdapter


class CustomChatbotTest(TestCase):

    def setUp(self):
        self.custom_chat_bot = CustomChatBot()

        api_key = '87654321-4321-4321-4321-210987654321'
        self.custom_chat_bot.api_key = api_key
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        # QUESTO MEDOTO VIENE ESEGUITO PRIMA DI TUTTI I TEST E LE DUE RIGHE SOTTOSTANI ELIMINANO I CHECK-IN
        # PRECEDENTI, IN MODO TALE DA NON AVERE DEI CONFLITTI DI RISPOSTE, INVALIDANDO I TEST
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.delete(url, headers={"api_key": api_key, "Content-Type": "application/json"}, timeout=10)

    def test_check_select_adapter(self):
        """Test per verificare la selezione della risposta da un adapter"""
        self.assertEqual(self.custom_chat_bot.select_response(Statement("ciao")).text,
                         DefaultAdapter.hello_response)

    def test_processing_stages_adapter(self):
        """Test per verificare che venga selezionato lo stesso adapter se l'operazione non è ancora terminata"""
        self.custom_chat_bot.select_response(Statement("check-in"))
        self.assertEqual(self.custom_chat_bot.select_response(Statement("check-out")).text,
                         CheckInAdapter.wrong_sede_response + "\n" + CheckInAdapter.sede_response)

    def test_reset_selected_adapter(self):
        """Test per verificare che venga deselezionato un adapter se ha finito di processare la richiesta"""
        self.custom_chat_bot.select_response(Statement("check-in"))
        self.custom_chat_bot.select_response(Statement("imola"))
        self.assertIsNone(self.custom_chat_bot.selected_adapter)

    def test_multiple_responses(self):
        """Test per verificare nel caso in cui vengano selezionate più risposte con la stessa 'confidence' venga
        ritornato un errore"""
        self.assertEqual(self.custom_chat_bot.select_response(Statement("check-in check-out")).text,
                         CustomChatBot.too_much_keywords_response)

    def test_selected_adapter_cant_process(self):
        """Test per verificare il corretto funzionamento del sistema nel caso in cui l'adapter selezionato non riesca a
        processare l'input"""
        self.custom_chat_bot.select_response(Statement("check-in"))
        self.custom_chat_bot.selected_adapter.reset_processing_stage()
        self.assertEqual(self.custom_chat_bot.select_response(Statement("imola")).text,
                         CustomChatBot.processing_error_response)
