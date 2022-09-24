from django.test import TestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chat.adapters.default_adapter import DefaultAdapter
from chat import settings


class DefaultAdapterTest(TestCase):
    chatterbot = None
    adapter = None

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.adapter = DefaultAdapter(self.chatterbot)

    def test_there_is_default_adapter(self):
        """TU66: Test per il controllo che esista default adapter."""
        adapter_types = []
        for logic_adapter in self.chatterbot.logic_adapters:
            adapter_types.append(type(logic_adapter))
        self.assertIn(DefaultAdapter, adapter_types)

    def test_correct_hello_word(self):
        """TU68: Test che verifica che venga riconosciuta una parola di saluto."""
        word = Statement('ciao')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, DefaultAdapter.hello_response)

    def test_incorrect_words(self):
        """TU85: Test che verifica che non venga riconosciuta alcuna parola chiave."""
        word = Statement('pollo')
        self.adapter.can_process(word)
        self.assertEqual(self.adapter.process(word).text, DefaultAdapter.default_message)
