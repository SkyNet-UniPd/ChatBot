import requests
from django.test import TestCase
from chat.requests.presence_request import PresenceRequest


class PresenceRequestTest(TestCase):

    def setUp(self):
        self.api_key = '87654321-4321-4321-4321-210987654321'
        self.presence_request = PresenceRequest(self.api_key)
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.delete(url, headers={"api_key": self.api_key, "Content-Type": "application/json"}, timeout=10)


    def test_send_presence_ok(self):
        """Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        requests.post(url, headers={"api_key": self.api_key, "Content-Type": "application/json"}, timeout=10)
        self.presence_request.send()
        self.assertEqual(self.presence_request.get_status(), "Ok")
