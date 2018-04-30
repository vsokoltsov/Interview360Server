from . import (User, TestCase, TransactionTestCase,
               RegistrationForm, mock, Token)

from django.test import override_settings
from rest_framework.authtoken.models import Token
from profiles.index import UserIndex
import ipdb


class RegistrationFormTests(TransactionTestCase):
    """ Tests for RegistrationForm object """

    def setUp(self):
        self.test_user = User(id=1)
        self.form_data = {
            'email': 'example@mail.com',
            'password': '12345678',
            'password_confirmation': '12345678'
        }

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form = RegistrationForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test form validation if parameters are missing. """

        form = RegistrationForm({})
        self.assertFalse(form.is_valid())

    def test_failed_form_validation_if_passwords_do_not_match(self):
        """ Test form validation in case mismatching the password """

        self.form_data['password_confirmation'] = '11111111'
        form = RegistrationForm(self.form_data)
        self.assertFalse(form.is_valid())

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_submit(self, user_index_mock):
        """ Test success call of submit """

        form = RegistrationForm(self.form_data)
        self.assertTrue(form.submit())

    def test_failed_submit(self):
        """ Test failed call of submit """

        form_data = {}
        form = RegistrationForm(form_data)
        self.assertFalse(form.submit())

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_user_creation(self, user_index_mock):
        """ Test success case of user creation """

        form = RegistrationForm(self.form_data)
        form.submit()
        last_user = User.objects.last()
        assert last_user.email == self.form_data['email']

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch.object(User, 'save')
    @mock.patch('django.contrib.auth.models.User')
    @mock.patch('rest_framework.authtoken.models.Token.objects.create')
    def test_failed_user_creation(self, index_mock, user_save_mock,
                                  user_class_mock, token_mock):
        """ Test failed case of user creation """

        form_data = {}
        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = self.test_user
        token_mock.user = self.test_user
        token_mock.return_value = "12345"
        user_save_mock.return_value = self.test_user

        form = RegistrationForm(form_data)
        form.submit()
        self.assertFalse(user_save_mock.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch('rest_framework.authtoken.models.Token.objects.create')
    def test_token_success_creation(self, index_mock, mock):
        """ Test token creation after success restore password """

        mock.user = self.test_user
        mock.return_value = return_value = ("12345", 12)

        form = RegistrationForm(self.form_data)
        form.submit()

        self.assertTrue(mock.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch('rest_framework.authtoken.models.Token.objects.create')
    def test_token_failed_creation(self, index_mock, mock):
        """ Test token creation after failed restore password """

        mock.user = self.test_user
        mock.return_value = ("12345", 12)
        form_data = {}
        form = RegistrationForm(form_data)
        form.submit()
        self.assertFalse(mock.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_index_success_creation(self, index_mock):
        """ Test success indexing of user information """

        form = RegistrationForm(self.form_data)
        form.submit()

        self.assertTrue(index_mock.called)
