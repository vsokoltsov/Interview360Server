from . import APITestCase, User

class RegistrationViewTests(APITestCase):
    """ Test of RegistrationViewSet class """

    def test_success_sign_up(self):
        """ Test success sign up with valid attributes """

        response = self.client.post('/api/v1/sign_up/', {
            'email': 'example@mail.com',
            'password': '12345678',
            'password_confirmation': '12345678'
        })
        self.assertEqual('token' in response.data, True)

    def test_failed_sign_up(self):
        """ Test failed sign up with invalid attributes """

        response = self.client.post('/api/v1/sign_up/', {
                    'email': '', 'password': ''
                })
        self.assertEqual('errors' in response.data, True)

    def test_failed_sign_up_user_already_exists(self):
        """ Test failed sign up if user already exists """

        user = User.objects.create(email="example@mail.com", password="12345678")
        response = self.client.post('/api/v1/sign_up/',  {
                'email': 'example@mail.com',
                'password': '12345678',
                'password_confirmation': '12345678'
        })
        self.assertEqual('errors' in response.data, True)
