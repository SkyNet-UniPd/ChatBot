from django.test import TestCase
from chat.requests.check_in_request import CheckInRequest


class CheckInRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.checkin_request = CheckInRequest(api_key)

    def test_send_checkin_ok(self):
        """TU04: Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.checkin_request.add_property('sede', 'IMOLA')
        self.checkin_request.send()
        self.assertEqual(self.checkin_request.get_status(), "Ok")

    def test_checkin_request_ready(self):
        """TU03: Test per verificare che la richiesta sia pronta se ci sono tutte le informazioni necessarie"""
        self.checkin_request.add_property('sede', 'IMOLA')
        self.checkin_request.sede = self.checkin_request.properties.get("sede")
        self.assertTrue(self.checkin_request.is_ready())

    def test_checkin_request_not_ready(self):
        """Test per verificare che la richiesta non sia pronta se non ci sono tutte le informazioni necessarie"""
        self.checkin_request.add_property('sede', None)
        self.assertFalse(self.checkin_request.is_ready())