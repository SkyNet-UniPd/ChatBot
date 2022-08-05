import datetime
import requests
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist, lev_dist_custom_dist
import re


class CheckOutAdapter(CustomLogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.sede = None
        self.date = datetime.date.today()

    def can_process(self, statement):
        check_out_words = ['check-out', 'checkout', 'check out', 'lasciare', 'andare via', 'tornare a casa', 'partire']

        #input_words = re.sub(r"[^a-zA-Z0-9 \n.\-/]", ' ', statement.text).split()
        input_words = statement.text.split()

        if self.processing_stage is not None:
            return True

        if lev_dist(input_words, check_out_words) or "?" in statement.text:
            self.processing_stage = "check-out"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        unauthorized_response = "Non hai ancora effettuato il login. Inserisci la tua API Key per proseguire con l'operazione di check-out"
        error_response = "Ops, qualcosa è andato storto... Riprova ad effettuare l'operazione"
        incorrect_response = "Non ho capito la tua richiesta..."
        location_confirm_response = "Effettuare il check-out per la sede di "
        #already_checked_out_response = "Hai già fatto il check-out!"
        not_checked_in_response = "Non è possibile effettuare il checkout perchè non risulti presente in alcuna sede."
        success_response = "Check-out effettuato correttamente per la sede di "
        exit_response = "Check-out annullato"

        # Test API Key
        api_key = '87654321-4321-4321-4321-210987654321'

        # Check if user wants to exit
        if self.check_exit(statement):
            self.processing_stage = None
            response = Statement(exit_response)
            response.confidence = 1
            return response

        # Check-out processing stages
        if self.processing_stage == "check-out":
            # Check if the user is already checked-out with API
            url = 'https://apibot4me.imolinfo.it/v1/locations/presence/me'
            service_response = requests.get(url, headers={'api_key': api_key})
            print("checkout imolinfo locations presence me: " + str(service_response.json()))  # LOG
            if service_response.status_code == 404:
                response_text = not_checked_in_response
                self.processing_stage = None
            else:
                self.processing_stage = "check-out confirm"
                self.sede = service_response.json()['location']
                response_text = location_confirm_response + self.sede + "?"
            confidence = 0.5
        elif self.processing_stage == "check-out confirm":
            yes_words = ["sì", "si", "ok", "yes", "s", "y", "vai"]
            no_words = ["no", "n", "nope"]
            if lev_dist_custom_dist(statement.text.split(), yes_words, 0):
                # Check-out the user in the selected 'sede' with API
                url = 'https://apibot4me.imolinfo.it/v1/locations/' + self.sede + '/presence'
                service_response = requests.delete(url, headers={"api_key": api_key,
                                                                 "Content-Type": "application/json"})
                self.processing_stage = None
                if service_response.status_code == 204:
                    response_text = success_response + self.sede
                else:
                    response_text = unauthorized_response + "\nError status code: " + str(service_response.status_code)
                    # + ": " + service_response.json()['error']
            elif lev_dist_custom_dist(statement.text.split(), no_words, 0):
                response_text = exit_response
                self.processing_stage = None
            else:
                response_text = incorrect_response + "\n" + location_confirm_response + self.sede + "?"
            confidence = 1
        else:  # Non dovrebbe mai arrivare qui
            self.processing_stage = None
            response_text = error_response
            confidence = 1

        response = Statement(response_text)
        response.confidence = confidence
        return response
