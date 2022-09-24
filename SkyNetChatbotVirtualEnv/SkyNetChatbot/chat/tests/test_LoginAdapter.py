from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat import settings
from chat.adapters.login_adapter import LoginAdapter


class LoginAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = LoginAdapter(self.chatterbot)
        self.api_key = '87654321-4321-4321-4321-210987654321'

    def test_there_is_login_adapter(self):
        """TU20: Test per il controllo che esista login adapter"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(LoginAdapter, adapters_types)

    def test_incorrect_process_login_words(self):
        """TU21: Test che riconosce la non correttezza del comando di login"""
        word = Statement('logoogi')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_login_words(self):
        """Test che riconosce la correttezza del comando di login"""
        word = Statement('login')
        self.assertTrue(self.adapter.can_process(word))

    def test_correct_process_api_question(self):
        """TU23: Test che verifica la richiesta di login"""
        word = Statement('login')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.login_response)

    def test_incorrect_process_login(self):
        """TU24: Test che controlla che l'operazione non venga effettuata correttamente"""
        self.adapter.processing_stage = "get api key"
        api_key = Statement('1')
        self.assertEqual(self.adapter.process(api_key).text, self.adapter.wrong_api_response)

    def test_check_api_key_ok(self):
        """TU25: Test per verificare che venga controllata l'api key"""
        self.assertTrue(self.adapter.check_api_key(self.api_key))

    def test_correct_process_login(self):
        """TU26: Test che controlla che l'operazione venga effettuata correttamente"""
        word = Statement('login')
        self.adapter.can_process(word)
        self.adapter.process(word)
        api_key = Statement(self.api_key)
        self.adapter.can_process(api_key)
        self.assertEqual(self.adapter.process(api_key).text, self.adapter.success_response)

    def test_already_login(self):
        """TU27: Test per verificare che non si possa fare il login se questo risulta già effettuato"""
        word = Statement('login')
        self.adapter.can_process(word)
        self.adapter.api_key = self.api_key
        self.assertEqual(self.adapter.process(word).text, self.adapter.already_login_response)

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot. """
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_check_api_key_no(self):
        """Test per verificare che venga controllata l'api key"""
        api_key = '1'
        self.assertFalse(self.adapter.check_api_key(api_key))

    def test_incorrect_login_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di login."""
        word = Statement('Pallone')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)
