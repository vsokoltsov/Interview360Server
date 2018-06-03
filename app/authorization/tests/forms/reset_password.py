from . import (User, TransactionTestCase,
               ResetPasswordForm, mock, Token)

import ipdb


class ResetPasswordFormTest(TransactionTestCase):
    """Tests for ResetPasswordForm."""

    def setUp(self):
        """Set up the test data."""

        user_params = {'email': 'example@mail.com'}
        self.user = User.objects.create(**user_params)
        self.user.set_password('12345678')
        self.token = Token.objects.create(user=self.user)

    def test_success_form_validation(self):
        """Test form validation if all necessary parameters are passed."""

        form_data = {
            'token': self.token.key,
            'password': '12345678',
            'password_confirmation': '12345678'
        }
        form = ResetPasswordForm(form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """Test failed form validation if params are missing."""

        form_data = {}
        form = ResetPasswordForm(form_data)
        self.assertFalse(form.is_valid())

    def test_success_submit(self):
        """Test success form submit."""

        form_data = {
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }
        form = ResetPasswordForm(form_data)
        self.assertTrue(form.submit())

    def test_failed_submit(self):
        """Test failed form submit."""

        form_data = {}
        form = ResetPasswordForm(form_data)
        self.assertFalse(form.submit())

    def test_user_changed_password(self):
        """Test success password changing."""

        form_data = {
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }
        form = ResetPasswordForm(form_data)
        form.submit()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(form_data['password']))

    def test_failed_submit_if_password_does_not_match(self):
        """Test failed submit if passwords does not match."""

        form_data = {
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'bbbbbb'
        }
        form = ResetPasswordForm(form_data)
        self.assertFalse(form.submit())

    def test_password_matching_error_key(self):
        """Test correct error key after password matching error."""

        form_data = {
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'bbbbbb'
        }
        form = ResetPasswordForm(form_data)
        form.submit()
        self.assertTrue('password_confirmation' in form.errors)
