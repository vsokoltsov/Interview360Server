from django.test import TestCase, TransactionTestCase
import mock
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember
from authorization.models import User
from companies.serializers import CompanySerializer
import datetime
import ipdb

class CompaniesListViewSetTests(APITestCase):
    """ API View tests for CompaniesListViewSet """



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

    def test_list_action(self):
        """ Test receiving of companies list """

        response = self.client.get('/api/v1/companies/')
        self.assertEqual(len(response.data['companies']), 1)

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


class CompanySerializerTests(TransactionTestCase):
    """ Tests for CompanySerializer class """

    def setUp(self):
        """ Setting up necessary dependencies """

        user = User.objects.create(email="example@mail.com", password="12345678")
        self.token = Token.objects.create(user=user)
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.date.today())
        company_member = CompanyMember.objects.create(user_id=user.id,
                                                      company_id=self.company.id,
                                                      role='owner')
        self.company_params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': datetime.date.today(),
            'owner_id': user.id
        }

        self.serializer = CompanySerializer(instance=self.company)

    def test_contains_expected_field(self):
        """ Test presence of serializer expected field """

        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'city',
                                                'description', 'start_date',
                                                'created_at', 'employees']))

    def test_success_validation_of_new_company(self):
        """ Test success case of creation of the new company """

        serializer = CompanySerializer(data=self.company_params)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation_of_new_company(self):
        """ Test failed case of creation of the new company """

        serializer = CompanySerializer(data={})
        self.assertFalse(serializer.is_valid())

    @mock.patch('companies.models.Company.objects.create')
    def test_success_company_creation(self, company_class_mock):
        """ Test success case of saving new Company """

        test_company = Company(id=1)
        company_class_mock.objects = mock.MagicMock()
        company_class_mock.objects.create = mock.MagicMock()
        company_class_mock.objects.create.return_value = test_company

        serializer = CompanySerializer(data=self.company_params)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(company_class_mock.called)

    @mock.patch('companies.models.CompanyMember.objects.create')
    def test_success_company_member_creation(self, company_member_mock):
        """ Test that CompanyMember objects was created just after the Company """
        
        test_company_member = CompanyMember(1)

        company_member_mock.objects = mock.MagicMock()
        company_member_mock.objects.create = mock.MagicMock()
        company_member_mock.objects.create.return_value = test_company_member

        serializer = CompanySerializer(data=self.company_params)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(company_member_mock.called)
