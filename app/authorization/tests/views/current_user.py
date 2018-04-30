from . import APITestCase, User
from rest_framework.authtoken.models import Token
import ipdb


class CurrentUserViewTests(APITestCase):
    """ Tests for current user receiving methods """

    def setUp(self):
        """ Set up test dependencies """

        user = User.objects.create(
            email="example@mail.com",
            password="12345678")
        self.token = Token.objects.create(user=user)

    def test_success_user_receiving(self):
        """ Test getting current user info if token is present """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/current/', format='json')
        self.assertEqual('current_user' in response.data, True)

    def test_failed_user_receiving(self):
        """ Test failed attempt of getting user if token is abscent """

        response = self.client.get('/api/v1/current/', format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual('detail' in response.data, True)
