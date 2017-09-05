from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime, COMPANY_OWNER
)

class CompaniesViewSetTests(APITestCase):
    """ API View tests for CompaniesViewSet """

    fixtures = [
        'user.yaml',
        'auth_token.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """ Set up test dependencies """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(COMPANY_OWNER)[0]
        self.token = Token.objects.get(user=self.user)
        company_member = CompanyMember.objects.get(
            user_id=self.user.id, company_id=self.company.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.company_params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': datetime.date.today(),
            'owner_id': self.user.id
        }

    def test_list_action(self):
        """ Test receiving of companies list """

        response = self.client.get('/api/v1/companies/')
        self.assertEqual(len(response.data), 1)

    def test_success_retrieve_action(self):
        """ Test receiving of particular company """

        response = self.client.get('/api/v1/companies/{}/'.format(self.company.id))
        self.assertEqual(response.status_code, 200)

    def test_success_create_action(self):
        """ Test success option of company's creation """

        response = self.client.post('/api/v1/companies/', self.company_params)
        self.assertTrue('company' in response.data)

    def test_failed_create_action(self):
        """ Test failed option of company's creation """

        response = self.client.post('/api/v1/companies/', {})
        self.assertTrue('errors' in response.data)

    def test_success_update_action(self):
        """ Test success option of company's update """

        url = '/api/v1/companies/{}/'.format(self.company.id)
        response = self.client.put(url, self.company_params)
        self.assertTrue('company' in response.data)

    def test_success_delete_action(self):
        """ Test success company deletion """

        url = '/api/v1/companies/{}/'.format(self.company.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
