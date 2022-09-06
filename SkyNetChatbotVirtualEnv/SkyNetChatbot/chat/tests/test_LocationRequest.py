from django.test import TestCase
from chat.requests.location_request import LocationRequest


class LocationRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.location_request = LocationRequest(api_key)

    def test_send_location_ok(self):
        """Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.location_request.send()
        self.assertEqual(self.location_request.get_status(), "Ok")
