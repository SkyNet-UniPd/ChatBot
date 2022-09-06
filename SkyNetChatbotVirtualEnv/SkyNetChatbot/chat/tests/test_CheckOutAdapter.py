from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
from chat.adapters.check_out_adapter import CheckOutAdapter
from chat.requests.check_out_request import CheckOutRequest
import requests


class CheckOutAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = CheckOutAdapter(self.chatterbot)
        api_key = '87654321-4321-4321-4321-210987654321'
        self.adapter.api_key = api_key
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.post(url, headers={"api_key": api_key, "Content-Type": "application/json"})

    def test_there_is_checkout_adapter(self):
        """TU11: Test per il controllo che esista check-out adapter"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(CheckOutAdapter, adapters_types)

    def test_incorrect_process_checkout_words(self):
        """TU12: Test che riconosce la non correttezza del comando di check out"""
        word = Statement('xhecl-oit')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_checkout_words(self):
        """Test che riconosce la correttezza del comando di check out"""
        word = Statement('check-out')
        self.assertTrue(self.adapter.can_process(word))

    def test_already_checkout(self):
        """TU14: Test per verificare che non si possa fare il check-out se non si è prima fatto il check-in"""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('sì')
        self.adapter.process(confirm)
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_checked_in_response)
    
    def test_confirm_checkout_location(self):
        """TU15: Test che verifica che il chatbot chieda conferma della sede per cui fare il checkout"""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.location_confirm_response +
                         self.adapter.sede + "?")

    def test_process_checkout(self):
        """TU16: Test per il controllo del successo dell'operazione di check-out inserendo tutte le info necessarie."""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('sì')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.success_response +
                         self.adapter.sede)

    def test_check_out_no_login(self):
        """TU17: Test per controllare che non sia possibile fare il checkout senza aver fatto login"""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_login_response)

    def test_no_confirm_checkout(self):
        """TU18: Test per il controllo dell'annullamento dell'operazione se non viene confermato il check-out"""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('no')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.exit_response)

    def test_incorrect_confirm_checkout(self):
        """Test per il controllo dell'annullamento dell'operazione se non viene confermato il check-out"""
        word = Statement('check-out')
        self.adapter.can_process(word)
        self.adapter.process(word)
        confirm = Statement('pollo')
        self.adapter.can_process(confirm)
        self.assertEqual(self.adapter.process(confirm).text, self.adapter.incorrect_response + "\n" +
                         self.adapter.location_confirm_response + self.adapter.sede + "?")

    def test_correct_processing_stage(self):
        """Test per il controllo che venga selezionato check-out adapter se l'operazione non è ancora terminata"""
        self.adapter.processing_stage = "check-out"
        self.assertTrue(self.adapter.can_process(Statement(None)))

    def test_incorrect_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di check-out."""
        word = Statement('check-in')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot. """
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_check_out_request_error(self):
        """Test per verificare che venga ritornato un errore se una richiesta API non va a buon fine"""
        word = Statement('check out')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")

    def test_check_presence(self):
        """Test per verificare che venga controllata la presenza in sede"""
        self.assertTrue(self.adapter.check_presence())

