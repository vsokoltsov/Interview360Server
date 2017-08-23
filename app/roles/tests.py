from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Role


class RolesViewSetTest(APITestCase):
    """ Tests for RoleViewSet class """

    def setUp(self):
        """ Setting up test dependencies """
        self.role = Role.objects.create(name='CEO')
        self.form_data = {
            'name': 'CTO'
        }


    def test_success_list_response(self):
        """ Test receiving of the roles list """

        response = self.client.get('/api/v1/roles/')
        self.assertEqual(len(response.data), 1)

    def test_success_retrieve_response(self):
        """ Test receiving of the detail information about role """

        response = self.client.get('/api/v1/roles/{}/'.format(self.role.id))
        self.assertEqual(response.data['id'], self.role.id)

    def test_success_role_creation(self):
        """ Test success creation of the role """

        response = self.client.post('/api/v1/roles/', self.form_data)
        self.assertEqual(int(response.data['id']), Role.objects.last().id)
        self.assertEqual(response.status_code, 201)

    def test_failed_role_creation(self):
        """ Test failed creation of the role """

        response = self.client.post('/api/v1/roles/', {})
        self.assertEqual(response.status_code, 400)

    def test_success_update_role(self):
        """ Test success update role """

        response = self.client.put(
            '/api/v1/roles/{}/'.format(self.role.id),
            { 'name': 'Tech lead' })
        self.assertEqual(response.status_code, 200)

    def test_failed_update_role(self):
        """ Test failed update role """

        response = self.client.put(
            '/api/v1/roles/{}/'.format(self.role.id),
            { })
        self.assertEqual(response.status_code, 400)

    def test_success_destroy(self):
        """ Test success role destroying """

        response = self.client.delete(
            '/api/v1/roles/{}/'.format(self.role.id)
        )
        self.assertEqual(response.status_code, 204)
