from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User
# Create your tests here.

class RegistrationViewTests(APITestCase):

    def test_success_sign_up(self):
        response = self.client.post('/api/v1/sign_up/', {'email': 'example@mail.com', 'password': '12345678'})
        self.assertEqual('token' in response.data, True)

    def test_failed_sign_up(self):
        response = self.client.post('/api/v1/sign_up/', {
                    'email': '', 'password': ''
                })
        self.assertEqual('errors' in response.data, True)

    def test_failed_sign_up_user_already_exists(self):
        user = User.objects.create(email="example@mail.com", password="12345678")
        response = self.client.post('/api/v1/sign_up/',  {
                'email': 'example@mail.com',
                'password': '12345678'
        })
        self.assertEqual('errors' in response.data, True)

class AuthorizationViewSetTests(APITestCase):

    def test_success_sign_in(self):
        """ Test success user sign in with valid credentials """
        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()
        
        response = self.client.post('/api/v1/sign_in/',  {
                'email': 'example@mail.com',
                'password': '12345678'
        })
        self.assertEqual('token' in response.data, True)
