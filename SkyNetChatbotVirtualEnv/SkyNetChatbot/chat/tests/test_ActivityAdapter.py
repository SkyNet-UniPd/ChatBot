import requests
from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat.adapters.activity_adapter import ActivityAdapter
from chat import settings


class ActivityAdapterTest(TestCase):
    chatterbot = None
    adapter = None

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = ActivityAdapter(self.chatterbot)
        self.api_key = '87654321-4321-4321-4321-210987654321'
        self.adapter.api_key = self.api_key
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.delete(url, headers={"api_key": self.api_key, "Content-Type": "application/json"}, timeout=10)

    def test_there_is_activity_adapter(self):
        """TU32: Test per il controllo che esista activity adapter."""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(ActivityAdapter, adapters_types)

    def test_incorrect_process_activity_words(self):
        """TU33: Test che riconosce la non correttezza del comando d'inserimento attività."""
        word = Statement('Impedisci attività')
        self.assertFalse(self.adapter.can_process(word))

    def test_invalid_format_billable_hours(self):
        """TU35: Test per il controllo inserimento attività inserendo le ore da consuntivare in un formato non valido."""
        self.adapter.processing_stage = "attività ore"
        billable_hours = Statement("a")
        response = self.adapter.process(billable_hours)
        self.assertEqual(response.text, self.adapter.ore_invalid_format_response + "\n" + self.adapter.ore_response)

    def test_correct_activity_and_project_question(self):
        """TU36: Test che verifica la comprensione di un inserimento attività e richiede l'ID del progetto per effettuare
        tale operazione."""
        word = Statement('Inserisci attività')
        self.adapter.can_process(word)
        response = self.adapter.process(word)
        self.assertEqual(response.text, self.adapter.progetto_response)

    def test_right_project_and_ore_question(self):
        """TU37: Test per il controllo inserimento attività inserendo un progetto esistente e non terminato."""
        self.adapter.processing_stage = "attività progetto"
        project = Statement('TEST-SKYNET')
        response = self.adapter.process(project)
        self.assertEqual(response.text, self.adapter.selected_progetto_response + project.text +
                         "! \n" + self.adapter.ore_response)

    def test_sede_and_description_question(self):
        """TU38: Test per il controllo inserimento attività inserendo la sede."""
        self.adapter.processing_stage = "attività location"
        sede = Statement("Imola")
        response = self.adapter.process(sede)
        self.assertEqual(response.text, self.adapter.descrizione_response)

    def test_wrong_sede(self):
        """TUxx: Test per il controllo inserimento attività inserendo una sede sbagliata."""
        self.adapter.processing_stage = "attività location"
        sede = Statement("Roma")
        response = self.adapter.process(sede)
        self.assertEqual(response.text, self.adapter.wrong_sede_response)

    def test_billable_hours_and_sede_question(self):
        """TU39: Test per il controllo inserimento attività inserendo le ore da consuntivare in un formato valido."""
        self.adapter.processing_stage = "attività ore"
        billable_hours = Statement(8.0)
        response = self.adapter.process(billable_hours)
        self.assertEqual(response.text, self.adapter.sede_response)

    def test_wrong_project(self):
        """TU40: Test per il controllo inserimento attività inserendo un progetto inesistente."""
        self.adapter.processing_stage = "attività progetto"
        project = Statement('-')
        response = self.adapter.process(project)
        self.assertEqual(response.text, self.adapter.wrong_progetto_response + "\n" + self.adapter.progetto_response)

    def test_closed_project(self):
        """TU41: Test per il controllo inserimento attività inserendo un progetto già terminato."""
        self.adapter.processing_stage = "attività progetto"
        project = Statement('test')
        response = self.adapter.process(project)
        self.assertEqual(response.text, self.adapter.wrong_progetto_response + "\n" + self.adapter.progetto_response)

    def test_billable_hours_and_description_question(self):
        """TU43: Test per il controllo inserimento attività inserendo le ore da consuntivare in un formato valido e il luogo
        viene selezionato automaticamente dalla presenza in sede."""
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.post(url, headers={"api_key": self.adapter.api_key, "Content-Type": "application/json"}, timeout=10)
        self.adapter.processing_stage = "attività ore"
        billable_hours = Statement(7.5)
        response = self.adapter.process(billable_hours)
        self.assertEqual(response.text, self.adapter.descrizione_response)

    def test_process_activity_success(self):
        """TU44: Test per il controllo inserimento attività inserendo tutte le info necessarie."""
        word = Statement('Inserisci attività')
        self.adapter.can_process(word)
        self.adapter.process(word)
        project = Statement('TEST-SKYNET')
        self.adapter.process(project)
        billable_hours = Statement(8.0)
        self.adapter.process(billable_hours)
        sede = Statement("Imola")
        self.adapter.process(sede)
        description = Statement("Test unità SkyNet")
        response = self.adapter.process(description)
        self.assertEqual(response.text, self.adapter.success_response)

    def test_correct_process_activity_words(self):
        """Test che riconosce la correttezza del comando d'inserimento attività."""
        word = Statement('Inserisci attività')
        self.assertTrue(self.adapter.can_process(word))

    def test_activity_no_login(self):
        """TU45: Test che controlla che non venga permesso di inserire una nuova attività se prima non si è fatto il login"""
        word = Statement('inserisci attività')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_login_response)

    def test_correct_processing_stage(self):
        """Test per il controllo che venga selezionato activity adapter se l'operazione non è ancora terminata"""
        self.adapter.processing_stage = "attività"
        self.assertTrue(self.adapter.can_process(Statement(None)))

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot"""
        word = Statement('annulla')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_incorrect_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non d'inserimento attività."""
        word = Statement('check-in')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)

    def test_check_presence(self):
        """Test per verificare che venga controllata la presenza in sede"""
        self.assertFalse(self.adapter.check_presence())

    def test_check_project_ok(self):
        """TU46: Test per verificare che venga controllato il codice del progetto"""
        project = 'skynetTest'
        self.assertTrue(self.adapter.check_project(project))

    def test_check_project_no(self):
        """Test per verificare che venga controllato il codice del progetto"""
        project = 'test'
        self.assertFalse(self.adapter.check_project(project))

    def test_check_sede_ok(self):
        """TU47: Test per verificare che venga controllata la sede"""
        sede = 'imola'
        self.assertTrue(self.adapter.check_sede(sede))

    def test_check_sede_no(self):
        """Test per verificare che venga controllata la sede"""
        sede = 'roma'
        self.assertFalse(self.adapter.check_sede(sede))

    def test_activity_request_error(self):
        """Test per verificare che venga ritornato un errore se una richiesta API non va a buon fine"""
        self.adapter.processing_stage = "attività progetto"
        word = Statement('TEST-SKYNET')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")
