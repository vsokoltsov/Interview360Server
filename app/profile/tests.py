from rest_framework.test import APITestCase
from authorization.models import User
from rest_framework.authtoken.models import Token
import ipdb

class ProfileViewSetTest(APITestCase):
    """ Tests for ProfileViewSet class """

    def setUp(self):
        """ Setting up testing dependencies """

        self.user = User.objects.create(email="example1@mail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.form_data = {
            'email': 'awdawdwad@mail.ru',
            'first_name': 'aaaaa',
            'last_name': 'bbbbb'
        }

    def test_success_receiving_of_profile(self):
        """ Test success receiving current user information """

        response = self.client.get('/api/v1/users/{}/'.format(self.user.id))
        assert response.status_code, 200

    def test_success_update_profile(self):
        """ Test success update of the profile information """

        response = self.client.put(
            '/api/v1/users/{}/'.format(self.user.id),
            self.form_data
        )
        user = User.objects.get(id=self.user.id)
        assert user.email, self.form_data['email']

    def test_success_change_password_route(self):
        """ Test success password change """
        
        response = self.client.put(
            '/api/v1/users/{}/change_password/'.format(self.user.id),
            self.form_data
        )
