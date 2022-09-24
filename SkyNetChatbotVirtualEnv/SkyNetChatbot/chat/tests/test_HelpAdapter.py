from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat.adapters.help_adapter import HelpAdapter
from chat import settings


class HelpAdapterTest(TestCase):
    chatterbot = None
    adapter = None

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = HelpAdapter(self.chatterbot)

    def test_there_is_help_adapter(self):
        """TU69: Test per il controllo che esista default adapter."""
        adapter_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapter_types.append(type(logic_adapter))
        self.assertIn(HelpAdapter, adapter_types)

    def test_correct_help_word(self):
        """TU70: Test che verifica che venga riconosciuta una parola di saluto."""
        word = Statement('help')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, "<strong>ℹ️ Help - Aiuto</strong><br/> Questa è la lista di tutti comandi disponbili offerti da SkyNetChatbot:<br/> " + HelpAdapter.ulify(HelpAdapter, HelpAdapter.help_commands))
