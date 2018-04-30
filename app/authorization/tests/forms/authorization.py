from . import User, TestCase, AuthorizationForm


class AuthorizationFormTests(TestCase):
    """ Tests for AuthorizationForm class """

    def test_success_form_validation(self):
        """ Test form validation if all necessary parameters are passed. """

        form_data = {'email': 'example@mail.com', 'password': '12345678'}
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

        form_data = {'email': 'example@mail.com', 'password': '12345678'}
        form = AuthorizationForm(form_data)
        self.assertEqual(form.submit(), True)

    def test_failed_authorization(self):
        """ Test form object failed submit() call """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        form_data = {'email': 'example@mail.com', 'password': ''}
        form = AuthorizationForm(form_data)
        self.assertEqual(form.submit(), False)

    def test_form_success_submit_create_token(self):
        """ Test that token is generated after success form submit """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        form_data = {'email': 'example@mail.com', 'password': '12345678'}
        form = AuthorizationForm(form_data)
        form.submit()
        self.assertIsNotNone(form.token)

    def test_form_failed_submit_token_is_abscent(self):
        """ Test that token is not generated if form is not submited correctly """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        form_data = {'email': 'example@mail.com', 'password': ''}
        form = AuthorizationForm(form_data)
        form.submit()
        self.assertEqual(hasattr(form, 'token'), False)
