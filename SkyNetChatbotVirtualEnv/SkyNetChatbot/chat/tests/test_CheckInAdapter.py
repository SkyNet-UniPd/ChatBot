import requests
from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat import settings
from chat.adapters.check_in_adapter import CheckInAdapter


class CheckInAdapterTest(TestCase):
    chatterbot = None
    adapter = None

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = CheckInAdapter(self.chatterbot)
        api_key = '87654321-4321-4321-4321-210987654321'
        self.adapter.api_key = api_key
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.delete(url, headers={"api_key": api_key, "Content-Type": "application/json"}, timeout=10)

    # def tearDown(self):
    #     pass

    def test_there_is_checkin_adapter(self):
        """TU01: Test per il controllo che esista un adapter per il check-in"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(CheckInAdapter, adapters_types)

    def test_incorrect_process_checkin_words(self):
        """TU02: Test per non accettare richieste non pertinenti al check-in"""
        word = Statement('xheck-on')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_checkin_words(self):
        """Test che riconosce la correttezza del comando di check in."""
        word = Statement('check in')
        self.assertTrue(self.adapter.can_process(word))

    def test_correct_processing_stage_checkin(self):
        """Test per il controllo che venga selezionato check-in adapter se l'operazione non è ancora terminata"""
        self.adapter.processing_stage = "check-in"
        self.assertTrue(self.adapter.can_process(Statement(None)))

    def test_check_in_already_done_in_office(self):
        """TU05: Test che controlla di non permettere di fare il check-in se risulta già effettuato un check-in """
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.adapter.process(word)
        office = Statement('IMOLA')
        self.adapter.process(office)
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(office).text, self.adapter.checkin_done_response + self.adapter.sede)

    def test_correct_check_in_and_office_question(self):
        """TU06: Test che verifica la richiesta della sede dove effettuare il check-in"""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.sede_response)

    def test_check_in_wrong_office(self):
        """TU07: Test che controlla che venga ritornato un messaggio di errore nel caso la sede inserita sia insesistente"""
        self.adapter.processing_stage = "check-in sede"
        office = Statement('PADOVA')
        self.assertEqual(self.adapter.process(office).text, self.adapter.wrong_sede_response + "\n" +
                         self.adapter.sede_response)

    def test_check_sede_ok(self):
        """TU08: Test per verificare che venga controllata la sede"""
        sede = 'imola'
        self.assertTrue(self.adapter.check_sede(sede))

    def test_check_in_right_office(self):
        """TU09: Test che controlla la correttezza della sede inserita"""
        self.adapter.processing_stage = "check-in sede"
        office = Statement('IMOLA')
        self.assertEqual(self.adapter.process(office).text, self.adapter.success_response +
                         self.adapter.sede)

    def test_check_in_no_login(self):
        """TU10: Test che controlla che non venga permesso di fare il check-in se prima non si è fatto il login"""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_login_response)

    def test_incorrect_check_in_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di check-in."""
        word = Statement('Pallone')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)

    def test_check_in_request_error(self):
        """Test per verificare che venga ritornato un errore se una richiesta API non va a buon fine"""
        self.adapter.processing_stage = "check-in sede"
        word = Statement('imola')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot. """
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_check_sede_no(self):
        """Test per verificare che venga controllata la sede"""
        sede = 'roma'
        self.assertFalse(self.adapter.check_sede(sede))

    def test_check_presence(self):
        """Test per verificare che venga controllata la presenza in sede"""
        self.assertFalse(self.adapter.check_presence())
