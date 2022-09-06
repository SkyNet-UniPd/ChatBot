from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.logic import LogicAdapter

from chat import settings


class CustomChatBot:
    too_much_keywords_response = "Mi spiace, ma ho trovato più soluzioni per il tuo problema e non riesco a decidere " \
                                 "quale sia la più adatta! Riprova ad effettuare la richiesta cercando di essere più " \
                                 "preciso possibile"
    processing_error_response = "Mi dispiace, non sono riuscito a processare la richiesta! Per favore riprova"

    def __init__(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.selected_adapter = None
        self.previous_statement = None
        self.api_key = None

    def select_response(self, input_statement):

        results = []
        result = None
        max_confidence = -1

        input_statement.in_response_to = self.previous_statement

        if self.selected_adapter is None:
            for adapter in self.chatterbot.logic_adapters:                    
                if isinstance(adapter, LogicAdapter) and adapter.can_process(input_statement):
                    if isinstance(adapter, CustomLogicAdapter):
                        adapter.update_api_key(self.api_key)
                    output = adapter.process(input_statement)
                    results.append(output)

                    self.chatterbot.logger.info(
                        '{} selected "{}" as a response with a confidence of {}'.format(
                            adapter.class_name, output.text, output.confidence
                        )
                    )

                    if output.confidence > max_confidence:
                        result = output
                        self.selected_adapter = adapter
                        max_confidence = output.confidence
                    elif output.confidence == max_confidence:
                        if isinstance(adapter, CustomLogicAdapter):
                            self.selected_adapter.reset_processing_stage()
                            adapter.reset_processing_stage()
                        self.selected_adapter = None
                        result = Statement(self.too_much_keywords_response)
                        result.confidence = 1
                    else:
                        if isinstance(adapter, CustomLogicAdapter):
                            adapter.reset_processing_stage()
                else:
                    self.chatterbot.logger.info(
                        'Not processing the statement using {}'.format(adapter.class_name)
                    )
        elif isinstance(self.selected_adapter, LogicAdapter):
            if self.selected_adapter.can_process(input_statement):
                result = self.selected_adapter.process(input_statement)
                self.chatterbot.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        self.selected_adapter.class_name, result.text, result.confidence
                    )
                )
            else:
                if isinstance(self.selected_adapter, CustomLogicAdapter):
                    self.selected_adapter.reset_processing_stage()
                self.selected_adapter = None
                result = Statement(self.processing_error_response)
                result.confidence = 1

        if isinstance(self.selected_adapter, CustomLogicAdapter):
            if self.selected_adapter and self.selected_adapter.is_processing_stage_none():
                self.selected_adapter = None
        elif isinstance(self.selected_adapter, LogicAdapter):
            self.selected_adapter = None

        response = Statement(
            text=result.text,
            in_response_to=input_statement.text,
            conversation=input_statement.conversation,
            persona='bot:' + self.chatterbot.name
        )

        response.confidence = result.confidence
        self.previous_statement = response

        return response
