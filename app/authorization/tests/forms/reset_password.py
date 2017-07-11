from . import (User, TransactionTestCase,
               ResetPasswordForm, mock, Token)

import ipdb
class ResetPasswordFormTest(TransactionTestCase):
    """ Tests for ResetPasswordForm """

    def setUp(self):
        """ Setting up the test data """
        user_params = {'email': 'example@mail.com', 'password': '12345678' }
        user = User.objects.create(**user_params).save()
        # ipdb.set_trace()
        self.token, _ = Token.objects.create(user=user)

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = {
                     'token': self.token,
                     'password': '12345678',
                     'password_confirmation': '12345678'
                     }
        form = ResetPasswordForm(form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test failed form validation if params are missing """

        form_data = { }
        form = ResetPasswordForm(form_data)
        self.assertFalse(form.is_valid())

    def test_success_submit(self):
        """ Test success form submit """

        ipdb.set_trace()
        form_data = {
                     'token': self.token,
                     'password': 'aaaaaa',
                     'password_confirmation': 'aaaaaa'
                     }
        form = ResetPasswordForm(form_data)
        self.assertTrue(form.submit())
