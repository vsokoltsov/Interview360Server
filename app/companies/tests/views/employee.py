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
        self.company_params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': datetime.date.today(),
            'owner_id': user.id
        }

    def test_employees_list(self):
        """ Test receiving list of employeers """

        url = "/api/v1/companies/{}/employees/".format(self.company.id)
        response = self.client.get(url)
        self.assertEqual(len(response.data['employees']), 1)
