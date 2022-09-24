from chatterbot.conversation import Statement
from chat.lev_dist import lev_dist_custom_dist
from chat.requests.request_factory import LocationRequestCreator, RequestError
from chat.adapters.custom_logic_adapter import CustomLogicAdapter


def ulify(elements):
    string = "<ul>"
    for s in elements:
        string += "<li>" + str(s) + "</li>"
    string += "</ul>"
    return string


class LocationsAdapter(CustomLogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        list_words = ["lista", "elenco"]
        locations_words = ["sedi", "uffici"]

        input_words = statement.text.split()

        if (lev_dist_custom_dist(input_words, list_words, 1) and lev_dist_custom_dist(input_words, locations_words, 1)) or lev_dist_custom_dist(input_words, locations_words, 1):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):

        try:
            if self.api_key is None:
                response = Statement(self.not_login_response)
                response.confidence = 1
                return response

            locations = []
            location_request = LocationRequestCreator().get_request(self.api_key)
            request_response = location_request.send()
            if location_request.get_status() == "Ok":
                for item in request_response.json():
                    locations.append(item['name'])

            response = Statement(
                "<strong>🏢 Lista Sedi: </strong><br/> " + ulify(locations))
            response.confidence = 0.5
            return response
        except RequestError as error:
            self.processing_stage = None
            response = Statement(error.__str__())
            response.confidence = 1
            return response
