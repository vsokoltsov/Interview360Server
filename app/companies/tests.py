from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember
from authorization.models import User
from datetime import datetime
# Create your tests here.

class CompaniesListViewSetTests(APITestCase):
    """ API View tests for CompaniesListViewSet """

    def setUp(self):
        """ Set up test dependencies """

        user = User.objects.create(email="example@mail.com", password="12345678")
        self.token = Token.objects.create(user=user)
        company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.now())
        company_member = CompanyMember.objects.create(user_id=user.id,
                                                      company_id=company.id,
                                                      role='owner')

    def test_list_action(self):
        """ Test receiving of companies list """
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/companies/')
        self.assertEqual(len(response.data['companies']), 1)
