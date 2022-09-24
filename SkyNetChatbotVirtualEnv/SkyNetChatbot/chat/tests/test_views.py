from django.test import TestCase, Client
from django.urls import reverse
from chat.views import ChatterBotApiView


class ViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.api_key = 'rVeXERS/iI2xo3ri+bfgsOuM4gGsLPY6GnlEZ5JyOTplASh8/pbSUegx5HlxVEVY'
        self.view = ChatterBotApiView()

    def test_get_request(self):
        response = self.client.get(reverse("chatterbot"))
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        request = reverse("chatterbot")
        response = self.client.post(request, data={'api_key': self.api_key, 'text': 'ciao'}, content_type=
                                    "application/json")
        self.assertEqual(response.status_code, 200)

    def test_post_request_not_text(self):
        request = reverse("chatterbot")
        response = self.client.post(request, data={'api_key': self.api_key}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
