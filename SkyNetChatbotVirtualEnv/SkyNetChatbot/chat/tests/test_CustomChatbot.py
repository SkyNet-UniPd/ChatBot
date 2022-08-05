from django.test import TestCase
from chatterbot import ChatBot
from chat import settings
from chatterbot.conversation import Statement
import requests
from chat.custom_chatbot import CustomChatBot

helloResponse = "Ciao, sono SkyNetChatbot, un bot che ti aiuta a gestire il tuo lavoro.\n" \
                    "Chiedimi qualcosa e io cercherò di risponderti nel migliore dei modi.\n" \
                    "Per esempio, per effettuare il check-in dimmi semplicemente: 'check-in'.\n" \
                    "Al momento sono disponibili solo le funzioni di check-in e check-out!"

class CustomChatbotTest(TestCase):
    @classmethod
    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.selected_adapter = None
        self.previous_statement = Statement('ciao')

    def test_check_select_adapter(self):
        """Test per verificare la selezione di un adapter"""
        self.assertEqual(CustomChatBot.select_response(self,self.previous_statement).text,helloResponse)
        

        
