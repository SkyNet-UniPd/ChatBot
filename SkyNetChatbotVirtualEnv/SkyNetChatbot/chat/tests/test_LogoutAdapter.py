from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
from chat.adapters.logout_adapter import LogoutAdapter


class LogoutAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = LogoutAdapter(self.chatterbot)
        self.adapter.api_key = '87654321-4321-4321-4321-210987654321'

    def test_there_is_logout_adapter(self):
        """TU78: Test per il controllo che esista logout adapter"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(LogoutAdapter, adapters_types)

    def test_incorrect_process_logout_words(self):
        """TU79: Test che riconosce la non correttezza del comando di logout"""
        word = Statement('logrrrra')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_logout_words(self):
        """Test che riconosce la correttezza del comando di logout"""
        word = Statement('logout')
        self.assertTrue(self.adapter.can_process(word))

    def test_confirm_logout(self):
        """TU80: Test che verifica che il chatbot chieda conferma del logout"""
        word = Statement('logout')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.logout_confirm_response)

    def test_process_logout(self):
        """TU81/82: Test per il controllo del successo dell'operazione di logout inserendo tutte le info necessarie."""
        word = Statement('logout')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('sì')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.success_response)

    def test_already_logout(self):
        """TU83: Test per verificare che non si possa fare il logout se non risulta fatto il login"""
        word = Statement('logout')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.no_logged_user_response)

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot. """
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_no_confirm_logout(self):
        """TU84: Test per il controllo dell'annullamento dell'operazione se non viene confermato il logout"""
        word = Statement('logout')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('no')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.exit_response)

    def test_incorrect_confirm_logout(self):
        """Test per il controllo dell'annullamento dell'operazione se non viene confermato il logout"""
        word = Statement('logout')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('pollo')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.incorrect_response + "\n" +
                         self.adapter.logout_confirm_response + "?")

    def test_incorrect_logout_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di logout."""
        word = Statement('Pallone')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)
