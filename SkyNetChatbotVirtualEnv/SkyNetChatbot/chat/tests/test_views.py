from django.test import TestCase
from django.views.generic import View
from chat.views import ChatterBotApiView
from django.http import JsonResponse
import requests


class ViewsTest(TestCase):
    @classmethod
    def setUp(self):
        self.request = requests.get('https://apibot4me.imolinfo.it/v1/locations/presence/me', headers={"api_key": '87654321-4321-4321-4321-210987654321'})
        #self.view = ChatterBotApiView

    def test_post_request(self):
        #self.assertEqual(self.view.post(ChatterBotApiView.as_view(), self.request).status, 200)
        pass
