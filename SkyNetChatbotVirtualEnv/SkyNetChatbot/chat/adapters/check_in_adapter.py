import datetime
import requests

from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist, lev_dist_str_correct_w, lev_dist_custom_dist
import re


class CheckInAdapter(CustomLogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.sede = None
        self.date = datetime.date.today()

    def can_process(self, statement, additional_response_selection_parameters=None):
        check_in_words = ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro', 'presenza']

        input_words = re.sub(r"[^a-zA-Z0-9 \n.\-/]", ' ', statement.text).split()

        if self.processing_stage is not None:
            return True

        if lev_dist_custom_dist(input_words, check_in_words, 1):
            self.processing_stage = "check-in"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        wrong_sede_response = "La sede che hai inserito non esiste!"
        sede_response = "In quale sede vuoi effettuare il check-in?"
        checkin_done_response = "Hai già fatto il check-in nella sede di "
        api_error_response = "Errore nella richiesta dei dati! Verifica di aver inserito le credenziali corrette!"
        success_response = "Check-in effettuato correttamente nella sede di "
        exit_response = "Check-in annullato"

        # Test API Key
        api_key = '87654321-4321-4321-4321-210987654321'

        # Check if user wants to exit
        if self.check_exit(statement):
            self.processing_stage = None
            response = Statement(exit_response)
            response.confidence = 1
            return response

        # Check-in processing stages
        if self.processing_stage == "check-in":
            # Check if the user is already checked-in in one 'sede' with API
            url = 'https://apibot4me.imolinfo.it/v1/locations/presence/me'
            service_response = requests.get(url, headers={'api_key': api_key})
            print("checkin imolinfo locations presence me: " + str(service_response.json()))  # LOG
            if service_response.status_code == 200:
                response_text = checkin_done_response + service_response.json()['location']
                self.processing_stage = None
            else:
                self.processing_stage = "check-in sede"
                response_text = sede_response
            confidence = 0.5
        elif self.processing_stage == "check-in sede":
            # Check if the input is a valid 'sede' with API
            url = 'https://apibot4me.imolinfo.it/v1/locations'
            service_response = requests.get(url, headers={"api_key": api_key})
            print("checkin imolinfo locations: " + str(service_response.json()))  # LOG
            if service_response.status_code == 200:
                sedi = []
                for item in service_response.json():
                    sedi.append(item['name'])
                if lev_dist(statement.text.split(), sedi):
                    self.sede = lev_dist_str_correct_w(statement.text.split(), sedi)
                    # Check-in the user in the selected 'sede' with API
                    url = 'https://apibot4me.imolinfo.it/v1/locations/' + self.sede + '/presence'
                    service_response = requests.post(url, headers={"api_key": api_key,
                                                                   "Content-Type": "application/json"})
                    if service_response.status_code == 204:
                        response_text = success_response + self.sede
                    else:
                        response_text = api_error_response + "\nError status code: " + str(service_response.status_code)
                        # + ": " + service_response.json()['error']
                    self.processing_stage = None
                else:
                    response_text = wrong_sede_response + "\n" + sede_response
            else:
                response_text = api_error_response + "\nError status code: " + str(service_response.status_code)
                # + ": " + service_response.json()['error']
                self.processing_stage = None
            confidence = 1
        else:  # Non dovrebbe mai arrivare qui
            self.processing_stage = None
            response_text = "Errore interno! Riprovare ad effettuare l'operazione."
            confidence = 1

        response = Statement(response_text)
        response.confidence = confidence
        return response
