import datetime
import re
from chatterbot.conversation import Statement
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chat.lev_dist import lev_dist, lev_dist_str_correct_w, lev_dist_custom_dist
from chat.requests.activity_request import RequestError
from chat.requests.request_factory import ProjectRequestCreator, PresenceRequestCreator, LocationRequestCreator, \
    ActivityRequestCreator


class ActivityAdapter(CustomLogicAdapter):
    # Bot responses
    progetto_response = "Qual è l'ID del progetto per cui vuoi registrare l'attività?"
    selected_progetto_response = "Hai scelto il progetto "
    wrong_progetto_response = "Il progetto che hai inserito non esiste oppure è già stato chiuso!"
    ore_response = "Inserisci il numero di ore da registrare per il progetto "
    ore_invalid_format_response = "Mi dispiace ma non ho capito. Ricorda che devi inserire un numero e usare come " \
                                  "eventuale separatore per le cifre decimali il carattere \'.\'!"
    invalid_conversion_response = "Mi dispiace ma non sono riuscito a convertire il valore! Per favore riprova"
    sede_response = "Non riesco a rintracciare la tua presenza in sede. In quale sede hai svolto l'attività?"
    descrizione_response = "Scrivi una breve descrizione di quello che hai fatto:"
    success_response = "Inserimento attività eseguito correttamente!"
    exit_response = "Inserimento attività annullato"
    wrong_sede_response = "La sede che hai inserito non esiste! In quale sede hai svolto l'attività?"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.project = None
        self.billableHours = None
        self.sede = None
        self.notes = None

    def can_process(self, statement):
        activity_words = ['attività', 'attivita']
        verbs_words = ['consuntivare', 'registrare', 'inserire', 'inserisci', "inserimento", 'svolto', 'svolgere']

        input_words = statement.text.split()

        if self.processing_stage is not None:
            return True
        if not lev_dist(input_words, activity_words) or not lev_dist(input_words, verbs_words):
            return False
        else:
            self.processing_stage = "attività"
            return True

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'attività' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Activity processing stages
            if self.processing_stage == "attività":
                if self.api_key is None:
                    self.processing_stage = None
                    response = Statement(self.not_login_response)
                    response.confidence = 1
                    return response
                else:
                    #Test API key:  "87654321-4321-4321-4321-210987654321"
                    response_text = self.progetto_response
                    confidence = 0.5
                    self.processing_stage = "attività progetto"
            elif self.processing_stage == "attività progetto":
                if self.check_project(statement.text):
                    response_text = self.selected_progetto_response + self.project + "! \n" + self.ore_response
                    self.processing_stage = "attività ore"
                else:
                    response_text = self.wrong_progetto_response + "\n" + self.progetto_response
                confidence = 1
            elif self.processing_stage == "attività ore":
                # Check if the input is a valid number
                if not re.search(r'^\d+\.\d+$', statement.text) and not re.search(r'^\d+$', statement.text):
                    response_text = self.ore_invalid_format_response + "\n" + self.ore_response
                else:
                    try:
                        self.billableHours = (float(statement.text))
                        if self.check_presence():
                            response_text = self.descrizione_response
                            self.processing_stage = "attività descrizione"
                        else:
                            response_text = self.sede_response
                            self.processing_stage = "attività location"
                    except ValueError:
                        response_text = self.invalid_conversion_response + "\n" + self.ore_response
                confidence = 1
            elif self.processing_stage == "attività location":
                if self.check_sede(statement.text):
                    response_text = self.descrizione_response
                    self.processing_stage = "attività descrizione"
                    confidence = 1
                else:
                    response_text = self.wrong_sede_response
                    confidence = 1
            elif self.processing_stage == "attività descrizione":
                self.notes = statement.text
                request = ActivityRequestCreator().get_request(self.api_key)
                request.add_property("method", "POST")
                request.add_property("project", str(self.project))
                request.add_property("billableHours", self.billableHours)
                request.add_property("sede", self.sede)
                request.add_property("notes", self.notes)
                request.send()
                if request.get_status() == "Ok":
                    response_text = self.success_response
                else:
                    response_text = self.internal_error_response
                self.processing_stage = None
                confidence = 1
            else:  # Non dovrebbe mai arrivare qui
                self.processing_stage = None
                response_text = self.internal_error_response
                confidence = 1
        except RequestError as error:
            self.processing_stage = None
            response_text = error.__str__()
            confidence = 1

        response = Statement(response_text)
        response.confidence = confidence
        return response

    def check_project(self, text):
        projects = []
        project_request = ProjectRequestCreator().get_request(self.api_key)
        request_response = project_request.send()
        if project_request.get_status() == "Ok":
            for item in request_response.json():
                if item['endDate'] is None or item['endDate'] > datetime.date.today().strftime('%Y-%m-%d'):
                    projects.append(item['code'])
        if lev_dist_custom_dist(text.split(), projects, 1):
            self.project = lev_dist_str_correct_w(text.split(), projects)
            return True
        return False

    def check_presence(self):
        request = PresenceRequestCreator().get_request(self.api_key)
        request_response = request.send()
        if request.get_status() == "Ok":
            self.sede = str(request_response.json()['location'])
            return True
        elif request.get_status() == "NotFound":
            return False
        else:
            raise RequestError("InternalError")

    def check_sede(self, text: str):
        locations = []
        location_request = LocationRequestCreator().get_request(self.api_key)
        request_response = location_request.send()
        if location_request.get_status() == "Ok":
            for item in request_response.json():
                locations.append(item['name'])
        if lev_dist(text.split(), locations):
            self.sede = lev_dist_str_correct_w(text.split(), locations)
            return True
        return False
