from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User
from .forms import AuthorizationForm
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


    def test_failed_sign_in(self):
        """ Test user's sign in with invalid credentials """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        response = self.client.post('/api/v1/sign_in/',  {
                'email': 'example@mail.com',
                'password': ''
        })
        self.assertEqual('errors' in response.data, True)


class AuthorizationFormTests(TestCase):
    """ Tests for AuthorizationForm class """

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = { 'email': 'example@mail.com', 'password': '12345678' }
        form = AuthorizationForm(form_data)
        self.assertEqual(form.is_valid(), True)

    def test_failed_form_validation(self):
        """ Test form validation if parameters are missing. """

        form = AuthorizationForm({})
        self.assertEqual(form.is_valid(), False)

    def test_success_authorization(self):
        """ Test form object success submit() call """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        form_data = { 'email': 'example@mail.com', 'password': '12345678' }
        form = AuthorizationForm(form_data)
        self.assertEqual(form.submit(), True)

    def test_failed_authorization(self):
        """ Test form object failed submit() call """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        form_data = { 'email': 'example@mail.com', 'password': '' }
        form = AuthorizationForm(form_data)
        self.assertEqual(form.submit(), False)
