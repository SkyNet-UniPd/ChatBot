from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
from chat.adapters.presence_adapter import PresenceAdapter
import requests


class PresenceAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = PresenceAdapter(self.chatterbot)
        api_key = '87654321-4321-4321-4321-210987654321'
        self.adapter.api_key = api_key

    def test_there_is_presence_adapter(self):
        """TU28: Test per il controllo che esista presence adapter"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(PresenceAdapter, adapters_types)

    def test_incorrect_process_presence_words(self):
        """TU29: Test che riconosce la non correttezza del comando di visualizzazione stato presenza"""
        word = Statement('presekto')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_presence_words(self):
        """Test che riconosce la correttezza del comando di visualizzazione stato presenza"""
        word = Statement('presenza')
        self.assertTrue(self.adapter.can_process(word))

    def test_presence_found(self):
        """TU30: Test che controlla che l'utente risulti presente in una sede"""
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.post(url, headers={"api_key": self.adapter.api_key, "Content-Type": "application/json"})
        word = Statement('presenza')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.present_response + self.adapter.sede + '.')

    def test_presence_no_login(self):
        """TU31: Test per controllare che non sia possibile visualizzare lo stato della presenza senza aver fatto login"""
        word = Statement('presenza')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_login_response)

    def test_presence_not_found(self):
        """Test che controlla che l'utente non risulti presente in alcuna sede"""
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.delete(url, headers={"api_key": self.adapter.api_key, "Content-Type": "application/json"})
        word = Statement('presenza')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_present_response)

    def test_incorrect_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di visualizzazione presenza."""
        word = Statement('check-in')
        # self.adapter.can_process(word)  # False
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)

    def test_presence_request_error(self):
        """Test per verificare che venga ritornato un errore se una richiesta API non va a buon fine"""
        word = Statement('presenza')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")

    def test_check_presence(self):
        """Test per verificare che venga controllata la presenza in sede"""
        self.assertFalse(self.adapter.check_presence())

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot. """
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

