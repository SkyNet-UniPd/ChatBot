from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat.adapters.projects_adapter import ProjectsAdapter
from chat import settings


class ProjectsAdapterTest(TestCase):

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = ProjectsAdapter(self.chatterbot)
        api_key = '87654321-4321-4321-4321-210987654321'
        self.adapter.api_key = api_key

    def test_there_is_projects_adapter(self):
        """TU95: Test per il controllo che esista projects adapter."""
        adapter_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapter_types.append(type(logic_adapter))
        self.assertIn(ProjectsAdapter, adapter_types)

    def test_correct_process_proj_words(self):
        """TU96: Test che verifica che venga riconosciuta la richiesta."""
        word = Statement('lista progetti')
        self.assertTrue(self.adapter.can_process(word))

    def test_list_projects_not_login(self):
        """TU97: Test che verifica che non venga effettuata l'operazione se l'utente non ha eseguito il login."""
        word = Statement('lista progetti')
        self.adapter.api_key = None
        response = self.adapter.process(word)
        self.assertEqual(self.adapter.not_login_response, response.text)

    def test_list_projects_success(self):
        """TU98: Test che verifica che la richiesta sie eseguita con successo."""
        word = Statement('lista progetti')
        response = self.adapter.process(word)
        self.assertIn("<strong>🚧 Lista Progetti: </strong><br/>", response.text)

    def test_list_projects_request_error(self):
        """Test che verifica che avvenga un errore con api-key sbagliata."""
        word = Statement('lista progetti')
        self.adapter.can_process(word)
        self.adapter.api_key = "1"
        response = self.adapter.process(word)
        self.assertEqual(response.text, "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")
