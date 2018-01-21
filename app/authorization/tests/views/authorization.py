from . import APITestCase, User

class AuthorizationViewSetTests(APITestCase):
    """ Test of AuthorizationViewSet class """

    def test_success_sign_in(self):
        """ Test success user sign in with valid credentials """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        response = self.client.post('/api/v1/sign_in/',  {
                'email': 'example@mail.com',
                'password': '12345678'
        }, format='json')
        self.assertEqual('token' in response.data, True)

    def test_failed_sign_in(self):
        """ Test user's sign in with invalid credentials """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        response = self.client.post('/api/v1/sign_in/',  {
                'email': 'example@mail.com',
                'password': ''
        }, format='json')
        self.assertEqual('errors' in response.data, True)
