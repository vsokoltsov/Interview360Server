from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.
import ipdb

class RegistrationViewTests(APITestCase):

    def test_success_sign_up(self):
        response = self.client.post('/api/v1/sign_up/', {'email': 'example@mail.com', 'password': '12345678'})
        self.assertEqual('token' in response.data, True)
