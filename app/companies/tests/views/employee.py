from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime,
    COMPANY_OWNER, HR, FileSystemStorage
)

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
        self.token = Token.objects.get(user=self.user)
        company_member = CompanyMember.objects.get(
            user_id=self.user.id, company_id=self.company.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.form_data = {
            'emails': [
                'example1@mail.com',
                'example2@mail.com',
                'example3@mail.com'
            ],
            'company_id': self.company.id,
            'role': HR
        }

    def test_employees_list(self):
        """ Test receiving list of employeers """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.get(url)
        self.assertEqual(len(response.data['employees']), 8)

    def test_success_employee_creation(self):
        """ Test success creation of the new employees """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.post(url, self.form_data)
        self.assertEqual('message' in response.data, True)

    def test_failed_employee_creation(self):
        """ Test failed creation of the new employees """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.post(url, {})
        self.assertTrue('errors' in response.data)
        self.assertEqual(response.status_code, 400)

    def test_success_company_member_deletion(self):
        """ Test success response of deletion the CompanyMember instance """

        url = "/api/v1/companies/{}/employees/{}/".format(self.company.id, self.user.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
