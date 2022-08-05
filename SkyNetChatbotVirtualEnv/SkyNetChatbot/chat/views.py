import json

from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse
from chatterbot.conversation import Statement
from chat.adapters.default_adapter import DefaultAdapter

from .train import ChatterBotTraining

from chat.custom_chatbot import CustomChatBot

import logging

logging.basicConfig(level=logging.CRITICAL)


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatbot = CustomChatBot()

    ChatterBotTraining(chatbot.chatterbot)

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        input_statement = Statement(input_data['text'])

        self.response = self.chatbot.select_response(input_statement)

        response_data = self.response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """

        return JsonResponse({
            'name': self.chatbot.chatterbot.name,
            'text': DefaultAdapter.helloResponse,
        }, status=200)
