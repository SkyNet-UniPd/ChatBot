from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
import requests
# from chat.check_in_adapter import can_process


class CheckInAdapterTest(TestCase):
    @classmethod
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = self.chatterbot.logic_adapters[0]

        api_key = '87654321-4321-4321-4321-210987654321'
        # *IMPORTANTE*
        # NON CAMBIARE QUESTO LINK, SI PRESUPPONE CHE TUTTI I TEST SIANO EFFETTUATI NELLA SEDE 'IMOLA'
        # QUESTO MEDOTO VIENE ESEGUITO PRIMA DI TUTTI I TEST E LE DUE RIGHE SOTTOSTANI ELIMINANO I CHECK-IN
        # PRECEDENTI, IN MODO TALE DA NON AVERE DEI CONFLITTI DI RISPOSTE, INVALIDANDO I TEST
        url = 'https://apibot4me.imolinfo.it/v1/locations/IMOLA/presence'
        service_response = requests.delete(url, headers={"api_key": api_key, "Content-Type": "application/json"})

    # def tearDown(self):
    #     pass

    def test_there_is_adapter(self):
        """Test per il controllo che esista almento un adapter"""
        self.assertIsNotNone(self.adapter)

    def test_correct_process_words(self):
        """Test che riconosce la correttezza del comando di check in. Le parole acettate sono ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro', 'presenza']"""
        word = Statement('check-in')
        self.assertEqual(self.adapter.can_process(word), True)

    def test_incorret_process_words(self):
        """Test che riconosce la non correttezza del comando di check in. Le parole acettate sono ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro', 'presenza']"""
        word = Statement('xheck-on')
        self.assertEqual(self.adapter.can_process(word), False)

    def test_exit_command(self):
        """Test che riconosce il comando di interrompere il bot. Per eseguire tale comando le parole acettate sono ['esci', 'chiudi', 'annulla', 'stop', 'fine', 'exit']"""
        word = Statement('exit')
        self.assertEqual(self.adapter.process(word).text, 'Check-in annullato')

    def test_corret_check_in_and_office_question(self):
        """Test che verifica la comprensione di un check in e richiede la sede per tale operazione. Le parole acettate sono ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro', 'presenza']"""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, 'In quale sede vuoi effettuare il check-in?')

    def test_incorret_check_in_command(self):
        """Test che verifica la comprensione di un check in. Le parole acettate sono ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro', 'presenza']"""
        word = Statement('Pallone')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, "Errore interno! Riprovare ad effettuare l'operazione.")

    def test_check_in_right_office(self):
        """Test per il controllo di un check in selezionando un ufficio esistente."""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.adapter.process(word)
        office = Statement('IMOLA')
        self.assertEqual(self.adapter.process(office).text, 'Check-in effettuato correttamente nella sede di ' + office.text)

    def test_check_in_wrong_office(self):
        """Test per il controllo di un check in selezionando un ufficio inesistente."""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.adapter.process(word)
        office = Statement('PADOVA')
        self.assertEqual(self.adapter.process(office).text, 'La sede che hai inserito non esiste!\nIn quale sede vuoi effettuare il check-in?')

    def test_check_in_already_done_in_office(self):
        """Test per il controllo di un check in precedentemente effettuato in un determinato ufficio"""
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.adapter.process(word)
        office = Statement('IMOLA')
        self.adapter.process(office)
        word = Statement('check-in')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(office).text, 'Hai già fatto il check-in nella sede di ' + office.text)

    def test_check_internal_error_message(self):
        """Test per il controllo del ritorno del messaggio di errore interno"""
        word = Statement('Pallone')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, 'Errore interno! Riprovare ad effettuare l\'operazione.')
