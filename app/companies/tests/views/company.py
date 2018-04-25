from . import (
    APITestCase, Company, CompanyMember, User,
    Token, datetime, COMPANY_OWNER, mock, CompanyIndex,
    CompanyFactory, CompanyMemberFactory, UserFactory
)
import ipdb

class CompaniesViewSetTests(APITestCase):
    """ API View tests for CompaniesViewSet """

    def setUp(self):
        """ Set up test dependencies """

        self.company = CompanyFactory()
        self.user = UserFactory()
        self.company_member = CompanyMemberFactory(
            user_id=self.user.id,
            company_id=self.company.id,
            role=COMPANY_OWNER
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.company_params = {
            'name': 'NAME',
            'city': 'City',
            'country': 'Country',
            'start_date': '2015-02-01',
            'owner_id': self.user.id
        }

    def test_list_action(self):
        """ Test receiving of companies list """

        response = self.client.get('/api/v1/companies/', format='json')
        self.assertEqual(len(response.data), 1)

    def test_success_retrieve_action(self):
        """ Test receiving of particular company """

        response = self.client.get(
            '/api/v1/companies/{}/'.format(self.company.id), format='json'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_create_action(self, index_mock, company_index):
        """ Test success option of company's creation """

        response = self.client.post(
            '/api/v1/companies/', self.company_params, format='json'
        )
        self.assertTrue('company' in response.data)

    def test_failed_create_action(self):
        """ Test failed option of company's creation """

        response = self.client.post('/api/v1/companies/', {}, format='json')
        self.assertTrue('errors' in response.data)

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch('companies.index.CompanyIndex.store_index')
    def test_success_update_action(self, company_index, user_index):
        """ Test success option of company's update """

        url = '/api/v1/companies/{}/'.format(self.company.id)
        response = self.client.put(url, self.company_params, format='json')
        self.assertTrue('company' in response.data)

    @mock.patch.object(CompanyIndex, 'get')
    @mock.patch.object(CompanyIndex, 'delete')
    @mock.patch('companies.index.CompanyIndex.store_index')
    def test_success_delete_action(self, company_index, compant_delete, company_get):
        """ Test success company deletion """

        url = '/api/v1/companies/{}/'.format(self.company.id)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)

    @mock.patch('companies.search.CompanySearch.find')
    def test_search_action(self, search_mock):
        """ Test success search of company """

        user_index = [
            { 'id': 1 },
            { 'id': 2 },
            { 'id': 3 }
        ]
        search_mock.return_value = user_index
        url = "/api/v1/companies/search/?q={}".format(
            'buzzword'
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['companies'], user_index)

    def test_absence_user_in_particular_company(self):
        """ Test unauthorized access if user does not belong to the company """

        user = User.objects.last()
        company_params = {
            'name': 'AAA',
            'city': 'BBB',
            'country': 'CCC',
            'start_date': datetime.date.today()
        }
        company = Company.objects.create(**company_params)
        response = self.client.get(
            '/api/v1/companies/{}/'.format(company.id), format='json'
        )
        assert response.status_code, 404

    def test_receiving_companies_filters(self):
        """ Test receiving of the companies filters """

        response = self.client.get('/api/v1/companies/filters/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('order' in response.data['filters'])
        self.assertTrue('roles' in response.data['filters'])

    @mock.patch('common.services.cities_service.CitiesService.find_by_name')
    def test_receiving_cities(self, cities_mock):
        """ Test receiving of the cities """

        cities = [
            { 'id': 1, 'name': 'Moscow' }
        ]
        cities_mock.return_value = cities

        response = self.client.get(
            '/api/v1/companies/cities/?name={}'.format('Moscow'),
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cities' in response.data)
        self.assertTrue(len(response.data['cities']) > 0)
