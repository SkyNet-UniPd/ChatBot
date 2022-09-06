import requests


class RequestError(Exception):

    def __init__(self, error=str("GenericError")):
        self.error_code = str(error)

    def __str__(self):
        if self.error_code.startswith("5"):
            return str("Errore nella comunicazione con il server! Verificare la propria connessione di rete. "
                       "Se il problema persiste riprova più tardi. Error " + self.error_code + " :(")
        elif self.error_code == "401":
            return str("Errore di autenticazione! Verifica di aver effettuato il login inserendo un api key "
                       "corretta! Error 401 - Unauthorized.")
        elif self.error_code == "InternalError" or self.error_code == "RequestNotImplemented" or \
                self.error_code == "RequestNotReady":
            return str("Ops, qualcosa è andato storto... Riprova ad effettuare l'operazione")
        elif self.error_code == "ConnectionError" or self.error_code.__contains__("Timeout"):
            return str("Errore di connessione! Verificare la propria connessione di rete. Se il problema persiste "
                       "riprova più tardi.")
        else:
            return str("Errore nella richiesta dei dati! Riprova più tardi. Error " + self.error_code + " :(")


class AbstractRequest:

    def __init__(self, api_key):
        self.api_key = api_key  # Test API Key: 87654321-4321-4321-4321-210987654321
        self.properties = dict()
        self.status = "Created"

    @staticmethod
    def send() -> requests.Response:
        """Metodo astratto che viene implementato dalle varie sottoclassi, se non viene ridefinito viene lanciata
        un'eccezione di tipo RequestError"""
        raise RequestError("RequestNotImplemented")

    def add_property(self, key, value):
        self.properties.__setitem__(key, value)

    def get_status(self):
        return self.status

