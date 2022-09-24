from django.test import TestCase
from chat.requests.abstract_request import AbstractRequest, RequestError


class AbstractRequestTest(TestCase):

    def setUp(self):
        api_key = '87654321-4321-4321-4321-210987654321'
        self.api_request = AbstractRequest(api_key)

    def test_error_500(self):
        """TU86: Test per verificare che venga notificato un error 500"""
        req = RequestError("500")
        self.assertEqual(req.__str__(), "Errore nella comunicazione con il server! Verificare la propria connessione di"
                                        " rete. Se il problema persiste riprova più tardi. Error 500 :(")
    
    def test_error_401(self):
        """TU87: Test per verificare che venga notificato un error 401"""
        req = RequestError("401")
        self.assertEqual(req.__str__(), "Errore di autenticazione! Verifica di aver effettuato il login inserendo un "
                                        "api key corretta! Error 401 - Unauthorized.")

    def test_internal_error(self):
        """TU88: Test per verificare che venga notificato un errore interno ignoto"""
        req = RequestError("InternalError")
        self.assertEqual(req.__str__(), "Ops, qualcosa è andato storto... Riprova ad effettuare l'operazione")

    def test_error_timeout(self):
        """TU89: Test per verificare che venga notificato un errore di timeout"""
        req = RequestError("Timeout")
        self.assertEqual(req.__str__(), "Errore di connessione! Verificare la propria connessione di rete. Se il "
                                        "problema persiste riprova più tardi.")

    def test_error_300(self):
        """TU90: Test per verificare che venga notificato un error 300"""
        req = RequestError("300")
        self.assertEqual(req.__str__(), "Errore nella richiesta dei dati! Riprova più tardi. Error " + req.error_code + " :(")

    def test_send_not_implemented(self):
        try:
            self.assertRaises(RequestError, self.api_request.send())
        except RequestError as e:
            self.assertEqual(e.error_code, "RequestNotImplemented")

    def test_add_property(self):
        self.api_request.add_property("test", "unit test")
        self.assertEqual(self.api_request.properties.get("test"), "unit test")

    def test_get_status(self):
        self.assertEqual(self.api_request.get_status(), "Created")
