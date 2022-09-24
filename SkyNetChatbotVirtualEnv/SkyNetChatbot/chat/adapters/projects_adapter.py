import datetime
from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist_custom_dist
from chat.requests.request_factory import ProjectRequestCreator, RequestError
from chat.adapters.custom_logic_adapter import CustomLogicAdapter


def ulify(elements):
    string = "<ul>"
    for s in elements:
        string += "<li>" + str(s) + "</li>"
    string += "</ul>"
    return string


class ProjectsAdapter(CustomLogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        list_words = ["lista", "elenco", "attivi"]
        projects_words = ["progetti", "progetto"]

        input_words = statement.text.split()

        if lev_dist_custom_dist(input_words, list_words, 1) and lev_dist_custom_dist(input_words, projects_words, 1):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        if self.api_key is None:
            response = Statement(self.not_login_response)
            response.confidence = 1
            return response

        try:
            projects = []
            project_request = ProjectRequestCreator().get_request(self.api_key)
            request_response = project_request.send()
            if project_request.get_status() == "Ok":
                for item in request_response.json():
                    if item['endDate'] is None or item['endDate'] > datetime.date.today().strftime('%Y-%m-%d'):
                        projects.append(item['code'])

            response = Statement(
                "<strong>🚧 Lista Progetti: </strong><br/> " + ulify(projects))
            response.confidence = 0.5
            return response
        except RequestError as error:
            self.processing_stage = None
            response = Statement(error.__str__())
            response.confidence = 1
            return response
