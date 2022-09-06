from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist, lev_dist_str_correct_w, lev_dist_custom_dist
import datetime
from chat.requests.request_factory import ProjectRequestCreator, ActivityRequestCreator
from chat.requests.activity_request import RequestError


class WorkedHoursAdapter(CustomLogicAdapter):
    wrong_project_response = "Il progetto che hai inserito non esiste oppure è stato chiuso!"
    project_response = "Di quale progetto vuoi sapere il totale delle ore consuntivate?"
    success_response = "Il totale delle ore consuntivate oggi per il progetto è: "
    exit_response = "Richiesta annullata"

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.project = None
        self.hours = 0

    def can_process(self, statement, additional_response_selection_parameters=None):
        cons_words = ['consuntivazione', 'consuntivate', 'totali', 'progetto', 'consuntivo']
        hours_words = ['ore', 'totale']

        input_words = statement.text.split()

        if self.processing_stage is not None:
            return True
        if lev_dist_custom_dist(input_words, hours_words, 1) and lev_dist(input_words, cons_words):
            self.processing_stage = "ore"
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        # Check if user wants to exit
        if self.processing_stage != 'ore' and self.check_exit(statement):
            self.processing_stage = None
            response = Statement(self.exit_response)
            response.confidence = 1
            return response

        try:
            # Ore totali processing stages
            if self.processing_stage == "ore":
                if self.api_key is None:
                    self.processing_stage = None
                    response = Statement(self.not_login_response)
                    response.confidence = 1
                    return response
                else:
                    response_text = self.project_response
                    confidence = 0.5
                    self.processing_stage = "ore progetto"
            elif self.processing_stage == "ore progetto":
                if self.check_project(statement.text):
                    self.hours = 0
                    request = ActivityRequestCreator().get_request(self.api_key)
                    request.add_property("project", str(self.project))
                    request.add_property("dateFilter", True)
                    response = request.send()
                    print("sended")
                    if request.get_status() == "Ok":
                        for item in response.json():
                            self.hours += item['billableHours']
                        response_text = self.success_response + str(self.hours)
                    else:
                        response_text = self.internal_error_response
                    self.processing_stage = None
                else:
                    response_text = self.wrong_project_response + "\n" + self.project_response
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

    def check_project(self, text: str):
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
        else:
            return False
