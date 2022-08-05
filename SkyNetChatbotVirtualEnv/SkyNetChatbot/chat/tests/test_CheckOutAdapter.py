from unittest import result
from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
from chat.adapters.check_out_adapter import CheckOutAdapter
import requests

class CheckOutAdapterTest(TestCase):
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = CheckOutAdapter(self.chatterbot)
        self.statement = Statement(None)

        api_key = '87654321-4321-4321-4321-210987654321'
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        # QUESTO MEDOTO VIENE ESEGUITO PRIMA DI TUTTI I TEST E LE DUE RIGHE SOTTOSTANI ELIMINANO I CHECK-IN
        # PRECEDENTI, IN MODO TALE DA NON AVERE DEI CONFLITTI DI RISPOSTE, INVALIDANDO I TEST
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        service_response = requests.post(url, headers={"api_key": api_key, "Content-Type": "application/json"})

    
    def test_there_is_adapter(self):
        """Test per il controllo che esista almento un adapter"""
        self.assertIsNotNone(self.adapter)

    def test_correct_process_checkout(self):
        """Test che riconosce la correttezza del comando di check out"""
        words = ['check-out', 'checkout', 'check out', 'lasciare', 'andare via', 'tornare a casa', 'partire']
        for w in words:
            self.statement.text = w
            self.assertEqual(self.adapter.can_process(self.statement), True)

    def test_incorrect_process_checkout(self):
        """Test per verificare che l'adapter non accetti parole non inerenti alla sua funzione"""
        words = ['check-in', 'sto entrando', 'ciao', 'arrivato', 'check in', 'checkin', 'entrato']
        for w in words:
            self.statement.text = w
            self.assertEqual(self.adapter.can_process(self.statement), False)

    def test_already_checkout(self):
        """Test per verificare che non si possa fare il checkout se non si è prima fatto il checkout"""
        self.statement.text = 'check-out'
        self.adapter.can_process(self.statement)
        self.adapter.process(self.statement)
        self.statement.text = 'IMOLA'
        self.adapter.process(self.statement)
        self.statement.text = 'check-out'
        self.adapter.can_process(self.statement)
        self.assertEqual(self.adapter.process(self.statement).text, "Non è possibile effettuare il checkout perchè non risulti presente in alcuna sede.")

    def test_exit_command(self):
        """Test che riconosce il comando di interrompere il bot"""
        words = ['esci', 'chiudi', 'annulla', 'stop', 'fine', 'exit']
        for w in words:
            self.statement.text = w
            self.assertEqual(self.adapter.process(self.statement).text, 'Check-out annullato')

    ''' def test_unauthorized_response(self):
        """Test che verifica che l'utente sia loggato per poter effettuare l'operazione"""
        self.statement.text = 'check-out'
        self.adapter.can_process(self.statement)
        self.adapter.process(self.statement)
        self.assertEqual(self.adapter.process(self.statement).text, "Non hai ancora effettuato il login. Inserisci la tua API Key per proseguire con l'operazione di check-out") '''

    def test_confirm_checkout_location(self):
        """Test che verifica che il chatbot chieda conferma della sede per cui fare il checkout"""
        self.statement.text = 'check-out'
        self.adapter.can_process(self.statement)
        self.assertEqual(self.adapter.process(self.statement).text, "Effettuare il check-out per la sede di IMOLA?")

    def test_process_checkout(self):
        """Test per verificare che si possa fare il checkout"""
        self.statement.text = 'check-out'
        self.adapter.can_process(self.statement)
        self.adapter.process(self.statement)
        self.statement.text = 'IMOLA'
        self.adapter.can_process(self.statement)
        self.assertEqual(self.adapter.process(self.statement).text, "Check-out effettuato correttamente per la sede di IMOLA")


