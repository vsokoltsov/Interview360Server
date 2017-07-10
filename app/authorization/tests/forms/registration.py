from . import (User, TestCase, TransactionTestCase,
               RegistrationForm, mock, Token)

from django.test import override_settings
from rest_framework.authtoken.models import Token
import ipdb

class RegistrationFormTests(TransactionTestCase):
    """ Tests for RegistrationForm object """

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = { 'email': 'example@mail.com', 'password': '12345678'}
        form = RegistrationForm(form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test form validation if parameters are missing. """

        form = RegistrationForm({})
        self.assertFalse(form.is_valid())

    def test_success_submit(self):
        """ Test success call of submit """

        form_data = { 'email': 'example@mail.com', 'password': '12345678'}
        form = RegistrationForm(form_data)
        self.assertTrue(form.submit())

    def test_failed_submit(self):
        """ Test failed call of submit """

        form_data = {}
        form = RegistrationForm(form_data)
        self.assertFalse(form.submit())

    @mock.patch.object(User, 'save')
    @mock.patch('django.contrib.auth.models.User')
    def test_success_user_creation(self, user_class_mock, user_save_mock):
        """ Test success case of user creation """
        test_user =  User(id=1)

        form_data = { 'email': 'example@mail.com', 'password': '12345678'}
        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = test_user
        Token.objects.create = mock.MagicMock(user=test_user,
                                                     return_value="12345")

        form = RegistrationForm(form_data)
        form.submit()
        self.assertTrue(user_save_mock.called)

    @mock.patch.object(User, 'save')
    @mock.patch('django.contrib.auth.models.User')
    def test_failed_user_creation(self, user_class_mock, user_save_mock):
        """ Test success case of user creation """
        test_user =  User(id=1)

        form_data = { }
        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = test_user
        Token.objects.create = mock.MagicMock(user=test_user,
                                                     return_value="12345")

        form = RegistrationForm(form_data)
        form.submit()
        self.assertFalse(user_save_mock.called)
