from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime, EMPLOYEE
)

class EmployeeActivationTests(APITestCase):
    """ Tests for EmployeeActivationTests """

    fixtures = [
        'user.yaml',
        'auth_token.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """ Setting up test credentials """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[-1]
        self.token = Token.objects.get(user=self.user)
        company_member = CompanyMember.objects.get(user_id=self.user.id, company_id=self.company.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.form_data = {
            'company_pk': self.company.id,
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }

    def test_success_employee_activation(self):
        """ Test success response for route """

        url = "/api/v1/companies/{}/activate_member/".format(self.company.id)
        response = self.client.put(url, self.form_data)
        self.assertTrue('message' in response.data)

    def test_failed_employee_activation(self):
        """ Test failed response for route """

        url = "/api/v1/companies/{}/activate_member/".format(self.company.id)
        response = self.client.put(url, {})
        self.assertTrue('errors' in response.data)
