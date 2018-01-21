from . import APITestCase, User, mock

class RegistrationViewTests(APITestCase):
    """ Test of RegistrationViewSet class """

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_sign_up(self, index_mock):
        """ Test success sign up with valid attributes """

        response = self.client.post('/api/v1/sign_up/', {
            'email': 'example@mail.com',
            'password': '12345678',
            'password_confirmation': '12345678'
        }, format='json')
        self.assertEqual('token' in response.data, True)

    def test_failed_sign_up(self):
        """ Test failed sign up with invalid attributes """

        response = self.client.post('/api/v1/sign_up/', {
                    'email': '', 'password': ''
                }, format='json')
        self.assertEqual('errors' in response.data, True)

    def test_failed_sign_up_user_already_exists(self):
        """ Test failed sign up if user already exists """

        user = User.objects.create(email="example@mail.com", password="12345678")
        response = self.client.post('/api/v1/sign_up/',  {
                'email': 'example@mail.com',
                'password': '12345678',
                'password_confirmation': '12345678'
        }, format='json')
        self.assertEqual('errors' in response.data, True)
