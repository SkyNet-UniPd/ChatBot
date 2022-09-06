from django.test import TestCase
from chat.requests.auth_request import AuthRequest


class AuthRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.auth_request = AuthRequest(api_key)

    def test_send_auth_ok(self):
        """TU22: Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.auth_request.send()
        self.assertEqual(self.auth_request.get_status(), "Ok")