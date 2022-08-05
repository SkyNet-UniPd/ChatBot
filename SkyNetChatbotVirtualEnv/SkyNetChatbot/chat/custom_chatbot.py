from chatterbot import ChatBot
from chatterbot.conversation import Statement

from chat import settings


class CustomChatBot:
    def __init__(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.selected_adapter = None
        self.previous_statement = None

    def select_response(self, input_statement):

        results = []
        result = None
        max_confidence = -1

        input_statement.in_response_to = self.previous_statement

        if self.selected_adapter is None:
            for adapter in self.chatterbot.logic_adapters:
                if adapter.can_process(input_statement):
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
                    else:
                        adapter.processing_stage = None
                else:
                    self.chatterbot.logger.info(
                        'Not processing the statement using {}'.format(adapter.class_name)
                    )
        else:
            result = self.selected_adapter.process(input_statement)
            self.chatterbot.logger.info(
                '{} selected "{}" as a response with a confidence of {}'.format(
                    self.selected_adapter.class_name, result.text, result.confidence
                )
            )

        if self.selected_adapter and self.selected_adapter.processing_stage is None:
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
