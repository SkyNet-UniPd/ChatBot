import json
import re
import logging
import base64
from django.views.generic import View
from django.http import JsonResponse
from chatterbot.conversation import Statement
from chat.adapters.default_adapter import DefaultAdapter
from chat.custom_chatbot import CustomChatBot
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

logging.basicConfig(level=logging.CRITICAL)


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatbot = CustomChatBot()

    def post(self, request):
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

        api_key = input_data['api_key']
        if api_key is not None:
            dec_apy_key = self.decrypt(api_key)
            self.chatbot.api_key = dec_apy_key
        else:
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

    def get(self, request):
        """
        Return data corresponding to the current conversation.
        """

        return JsonResponse({
            'name': self.chatbot.chatterbot.name,
            'text': DefaultAdapter.hello_response,
        }, status=200)

    def decrypt(self, enc):
        key = '2442264529482B4D'
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)
