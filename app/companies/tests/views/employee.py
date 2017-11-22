from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime,
    COMPANY_OWNER, HR, FileSystemStorage, mock, EMPLOYEE, CANDIDATE
)
from profiles.index import UserIndex

class EmployeesViewSetTests(APITestCase):
    """ API View tests for EmployeeViewSet """

    fixtures = [
        'user.yaml',
        'auth_token.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """ Set up test dependencies """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(COMPANY_OWNER)[0]
        self.employee = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.token = Token.objects.get(user=self.user)
        company_member = CompanyMember.objects.get(
            user_id=self.user.id, company_id=self.company.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.content_type = 'application/json'
        self.form_data = {
            'employees': [
                { 'email': 'example1@mail.com', 'role': CANDIDATE },
                { 'email': 'example2@mail.com', 'role': EMPLOYEE },
                { 'email': 'example3@mail.com', 'role': CANDIDATE }
            ],
            'company_id': self.company.id
        }
        self.update_form_data = {
            'email': 'example@mail.com',
            'first_name': 'Ololosh',
            'last_name': 'Ololoevich'
        }

    def test_employees_list(self):
        """ Test receiving list of employeers """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['employees']), 8)

    def test_employee_retrieving(self):
        """ Test receiving detail information about employee """

        url = "/api/v1/companies/{}/employees/{}/".format(
            self.company.id, self.employee.id
        )
        response = self.client.get(url, format='json')
        assert response.status_code, 200

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_employee_creation(self, user_index):
        """ Test success creation of the new employees """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.post(url, self.form_data, format='json')
        self.assertEqual('employees' in response.data, True)

    def test_failed_employee_creation(self):
        """ Test failed creation of the new employees """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.post(url, {}, format='json')
        self.assertTrue('errors' in response.data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_employee_update(self, user_index):
        """ Test success employee's instance update """

        url = "/api/v1/companies/{}/employees/{}/".format(
            self.company.id, self.employee.id
        )
        response = self.client.put(url, self.update_form_data, format='json')
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(UserIndex, 'get')
    @mock.patch.object(UserIndex, 'delete')
    def test_success_company_member_deletion(self, user_index, get_mock):
        """ Test success response of deletion the CompanyMember instance """

        url = "/api/v1/companies/{}/employees/{}/".format(self.company.id, self.user.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    @mock.patch('profiles.search.UsersSearch.find')
    def test_search_action(self, search_mock):
        """ Test success search of user inside particular company """

        user_index = [
            { 'id': 1 },
            { 'id': 2 },
            { 'id': 3 }
        ]
        search_mock.return_value = user_index
        url = "/api/v1/companies/{}/employees/search/?q={}".format(
            self.company.id, 'buzzword'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['users'], user_index)
