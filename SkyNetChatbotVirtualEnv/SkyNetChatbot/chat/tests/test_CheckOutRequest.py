from django.test import TestCase
from chat.requests.check_out_request import CheckOutRequest


class CheckOutRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.checkout_request = CheckOutRequest(api_key)

    def test_send_checkout_ok(self):
        """TU13: Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.checkout_request.add_property('sede', 'IMOLA')
        self.checkout_request.send()
        self.assertEqual(self.checkout_request.get_status(), "Ok")

    def test_checkout_request_ready(self):
        """TU19: Test per verificare che la richiesta sia pronta se ci sono tutte le informazioni necessarie"""
        self.checkout_request.add_property('sede', 'IMOLA')
        self.checkout_request.sede = self.checkout_request.properties.get("sede")
        self.assertTrue(self.checkout_request.is_ready())

    def test_checkout_request_not_ready(self):
        """Test per verificare che la richiesta non sia pronta se non ci sono tutte le informazioni necessarie"""
        self.checkout_request.add_property('sede', None)
        self.assertFalse(self.checkout_request.is_ready())