from . import APITestCase, User, Token

class ResetPasswordTest(APITestCase):
    """ Test ResetPasswordViewSet routes """

    def setUp(self):
        """ Setting up some user special settings """
        self.user = User.objects.create(email="example@mail.com")
        self.user.set_password('12345678')
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def test_success_reset(self):
        """ Succesfully reset user password """

        form_data = { 'password': '123456789',
                      'password_confirmation': '123456789',
                      'token': self.token.key
                    }
        response = self.client.post('/api/v1/reset_password/', form_data)
        self.assertTrue('message' in response.data)

    def test_failed_reset(self):
        """ Test failed attempt to reset user's password """

        form_data = { 'password': '123456789',
                      'password_confirmation': '123456789',
                      'token': ''
                    }
        response = self.client.post('/api/v1/reset_password/', form_data)
        self.assertTrue('errors' in response.data)
