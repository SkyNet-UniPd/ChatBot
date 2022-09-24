from django.test import TestCase
from chatterbot.conversation import Statement
from chatterbot.chatterbot import ChatBot
from chat import settings
from chat.adapters.custom_logic_adapter import CustomLogicAdapter


class CustomLogicAdapterTest(TestCase):

    def setUp(self):
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        self.cla = CustomLogicAdapter(self.chatterbot)

    def test_correct_exit_command(self):
        """TU67: Test per verificare il corretto funzionamento del comando annulla operazione"""
        self.assertEqual(self.cla.check_exit(Statement('annulla')), True)

    def test_matching_exit_command(self):
        self.assertEqual(self.cla.check_exit(Statement('chidi')), True)

    def test_non_matching_exit_command(self):
        self.assertEqual(self.cla.check_exit(Statement('chd')), False)

    def test_incorrect_exit_command(self):
        self.assertEqual(self.cla.check_exit(Statement('Pallone')), False)

    def test_reset_processing_stage(self):
        self.cla.processing_stage = "prova"
        self.cla.reset_processing_stage()
        self.assertIsNone(self.cla.processing_stage)

    def test_is_processing_stage_none(self):
        self.assertTrue(self.cla.is_processing_stage_none())

    def test_update_api_key(self):
        self.cla.update_api_key("1234-5678-90")
        self.assertEqual(self.cla.api_key, "1234-5678-90")
