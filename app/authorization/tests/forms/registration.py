from . import User, TestCase, RegistrationForm

from django.test import override_settings
from rest_framework.authtoken.models import Token

class RegistrationFormTests(TestCase):
    """ Tests for RegistrationForm object """

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = { 'email': 'example@mail.com', 'password': '12345678'}
        form = RegistrationForm(form_data)
        self.assertEqual(form.is_valid(), True)
