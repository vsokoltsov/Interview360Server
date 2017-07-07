from . import User, TestCase, RestorePasswordForm

from django.test import override_settings
import mock
import ipdb
import django.core.mail as mail

class RestorePasswordFormTests(TestCase):
    """ Test RestorePasswordForm class """

    def setUp(self):
        """ Setting up test credentials """
        self.user = User.objects.create(email="example@mail.com")
        self.user.set_password('12345678')
        self.user.save()

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = { 'email': 'example@mail.com'}
        form = RestorePasswordForm(form_data)
        self.assertEqual(form.is_valid(), True)

    def test_failed_form_validation(self):
        """ Test form validation if parameters are missing. """

        form = RestorePasswordForm({})
        self.assertEqual(form.is_valid(), False)

    def test_success_submit(self):
        """ Test success call of submit """

        form_data = { 'email': self.user.email }
        form = RestorePasswordForm(form_data)
        self.assertEqual(form.submit(), True)

    def test_failed_submit(self):
        """ Test failed call of submit """
        
        form_data = {}
        form = RestorePasswordForm(form_data)
        self.assertEqual(form.submit(), False)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_mail_was_sended(self):
        form_data = { 'email': 'example@mail.com'}
        form = RestorePasswordForm(form_data)
        form.submit()
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_mail_was_not_sended(self):
        form_data = {}
        form = RestorePasswordForm(form_data)
        form.submit()
        self.assertEqual(len(mail.outbox), 0)
