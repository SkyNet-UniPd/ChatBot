from django.test import TestCase
from chat.adapters.custom_logic_adapter import CustomLogicAdapter
from chatterbot.conversation import Statement


class CustomLogicAdapterTest(TestCase):
    @classmethod
    def setUp(self):
        self.clam = CustomLogicAdapter

    # def tearDown(self):
    #     pass

    def test_correct_exit_command(self):
        self.assertEqual(self.clam.check_exit(Statement('esci')), True)

    def test_matchig_exit_command(self):
        self.assertEqual(self.clam.check_exit(Statement('chidi')), True)

    def test_non_matchig_exit_command(self):
        self.assertEqual(self.clam.check_exit(Statement('chd')), False)

    def test_incorrect_exit_command(self):
        self.assertEqual(self.clam.check_exit(Statement('Pallone')), False)
