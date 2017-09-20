from rest_framework.test import APITestCase
from authorization.models import User
from rest_framework.authtoken.models import Token

class ProfileViewSetTest(APITestCase):
    """ Tests for ProfileViewSet class """

    def setUp(self):
        """ Setting up testing dependencies """

        self.user = User.objects.create(email="example1@mail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_success_receiving_of_profile(self):
        """ Test success receiving current user information """

        response = self.client.get('/api/v1/profile')
        assert response.status_code, 200
