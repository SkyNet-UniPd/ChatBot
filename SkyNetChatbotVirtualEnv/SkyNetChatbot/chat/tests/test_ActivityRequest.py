from django.test import TestCase
from chat.requests.activity_request import ActivityRequest


class ActivityRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.activity_request = ActivityRequest(api_key)

    def test_send_activity_ok(self):
        """TU34: Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.activity_request.add_property('project', '99')
        self.activity_request.add_property('billableHours', 2)
        self.activity_request.add_property('sede', 'IMOLA')
        self.activity_request.add_property('notes', "note")
        self.activity_request.add_property('method', "POST")
        self.activity_request.send()
        self.assertEqual(self.activity_request.get_status(), "Ok")

    def test_activity_request_ready(self):
        """TU42: Test per verificare che la richiesta sia pronta se ci sono tutte le informazioni necessarie"""
        self.activity_request.add_property('project', '99')
        self.activity_request.add_property('billableHours', 2)
        self.activity_request.add_property('sede', 'IMOLA')
        self.activity_request.add_property('method', "POST")
        self.activity_request.send()
        self.assertTrue(self.activity_request.is_ready())

    def test_activity_request_not_ready(self):
        """Test per verificare che la richiesta non sia pronta se non ci sono tutte le informazioni necessarie"""
        self.activity_request.add_property('project', None)
        self.activity_request.add_property('billableHours', None)
        self.activity_request.add_property('sede', None)
        self.assertFalse(self.activity_request.is_ready())

    def test_send_hours_ok(self):
        """TU51: Test per verificare che con tutti i dati necessari la richiesta venga spedita correttamente"""
        self.activity_request.add_property('project', '99')
        self.activity_request.add_property('dateFilter', True)
        self.activity_request.send()
        self.assertEqual(self.activity_request.get_status(), "Ok")
