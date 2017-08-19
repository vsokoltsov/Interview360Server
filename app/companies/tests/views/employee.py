from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime
)
import ipdb

class EmployeesViewSetTests(APITestCase):
    """ API View tests for EmployeeViewSet """

    def setUp(self):
        """ Set up test dependencies """

        user = User.objects.create(email="example@mail.com", password="12345678")
        self.token = Token.objects.create(user=user)
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        company_member = CompanyMember.objects.create(user_id=user.id,
                                                      company_id=self.company.id,
                                                      role='owner')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.form_data = {
            'emails': [
                'example1@mail.com',
                'example2@mail.com',
                'example3@mail.com'
            ],
            'company_id': self.company.id
        }

    def test_employees_list(self):
        """ Test receiving list of employeers """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.get(url)
        self.assertEqual(len(response.data['employees']), 1)

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
