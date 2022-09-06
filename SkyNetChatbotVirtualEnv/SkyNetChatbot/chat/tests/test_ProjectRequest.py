from django.test import TestCase
from chat.requests.project_request import ProjectRequest


class ProjectRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.project_request = ProjectRequest(api_key)

    def test_send_project_ok(self):
        """Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.project_request.send()
        self.assertEqual(self.project_request.get_status(), "Ok")