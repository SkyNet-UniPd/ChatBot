import json
import re

from django.views.generic import View
from django.http import JsonResponse
from chatterbot.conversation import Statement
from chat.adapters.default_adapter import DefaultAdapter

from chat.custom_chatbot import CustomChatBot

import logging

logging.basicConfig(level=logging.CRITICAL)


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatbot = CustomChatBot()

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

        self.chatbot.api_key = input_data['api_key']
        # 87654321-4321-4321-4321-210987654321
        
        # Creazione dello Statement in cui viene fatto un controllo dell'input dell'utente
        # Vengono sostituiti i caratteri speciali (@,%,$,ecc) con il carattere ' '
        # Poi ci si assicura che le parole valide siano separate da un singolo spazio
        text = re.sub(r"[^\w \n\-.]", ' ', str(input_data['text']))
        final_text = re.sub(r" +", " ", text)
        input_statement = Statement(final_text)

        response = self.chatbot.select_response(input_statement)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """

        return JsonResponse({
            'name': self.chatbot.chatterbot.name,
            'text': DefaultAdapter.hello_response,
        }, status=200)
