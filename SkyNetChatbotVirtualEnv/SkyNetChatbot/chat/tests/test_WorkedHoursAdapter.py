from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat import settings
from chat.adapters.worked_hours_adapter import WorkedHoursAdapter


class WorkedHoursAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = WorkedHoursAdapter(self.chatterbot)
        self.statement = Statement(None)
        self.adapter.api_key = '87654321-4321-4321-4321-210987654321'
    
    def test_there_is_worked_hours_adapter(self):
        """TU48: Test per il controllo che esista worked hours adapter"""
        adapters_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapters_types.append(type(logic_adapter))
        self.assertIn(WorkedHoursAdapter, adapters_types)

    def test_incorrect_process_working_hours_words(self):
        """TU49: Test per non accettare richieste non pertinenti alla sua funzione"""
        word = Statement('login')
        self.assertFalse(self.adapter.can_process(word))

    def test_correct_process_working_hours_words(self):
        """Test che riconosce la correttezza del comando di richiesta delle ore totali"""
        word = Statement('ore consuntivate')
        self.assertTrue(self.adapter.can_process(word))

    def test_wrong_project(self):
        """TU52: Test per il controllo che il progetto non sia inesistente."""
        self.adapter.processing_stage = "ore progetto"
        project = Statement('-')
        response = self.adapter.process(project)
        self.assertEqual(response.text, self.adapter.wrong_project_response + "\n" + self.adapter.project_response)

    def test_get_project_code(self):
        """TU53: Test che verifica che il chatbot chieda il codice del progetto per cui sapere le ore consuntivate"""
        word = Statement('ore consuntivate')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, self.adapter.project_response)

    def test_worked_hours_no_login(self):
        """TU54: Test che controlla che non venga permesso di sapere le ore consuntivate se prima non si è fatto il login"""
        word = Statement('ore consuntivate')
        self.adapter.can_process(word)
        self.adapter.api_key = None
        self.assertEqual(self.adapter.process(word).text, self.adapter.not_login_response)

    def test_check_project_ok(self):
        """TU55: Test per verificare che venga controllato il codice del progetto"""
        project = 'skynetTest'
        self.assertTrue(self.adapter.check_project(project))

    def test_check_project_no(self):
        """Test per verificare che venga controllato il codice del progetto"""
        project = 'test'
        self.assertFalse(self.adapter.check_project(project))

    def test_exit_command(self):
        """Test che riconosce il comando d'interruzione della richiesta effettuata al bot"""
        word = Statement('annulla')
        self.assertEqual(self.adapter.process(word).text, self.adapter.exit_response)

    def test_process_worked_hours(self):
        """TU56: Test per il controllo del successo dell'operazione di richiesta delle ore consuntivate inserendo tutte le info necessarie."""
        word = Statement('ore consuntivate')
        self.adapter.can_process(word)
        self.adapter.process(word)
        project = Statement('skynetTest')
        self.adapter.can_process(project)
        self.assertEqual(self.adapter.process(project).text, self.adapter.success_response + str(self.adapter.hours))

    def test_incorrect_worked_hours_command(self):
        """Test che verifica che si ritorni un errore se viene processato un comando non di richiesta delle ore consuntivate."""
        word = Statement('Pallone')
        self.assertEqual(self.adapter.process(word).text, self.adapter.internal_error_response)

    def test_worked_hours_request_error(self):
        """Test per verificare che venga ritornato un errore se una richiesta API non va a buon fine"""
        self.adapter.processing_stage = "ore progetto"
        word = Statement('1')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")
