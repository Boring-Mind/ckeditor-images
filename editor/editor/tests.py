from django.test import TestCase


class ImageLoad(TestCase):

    def test_return_error_on_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 404)