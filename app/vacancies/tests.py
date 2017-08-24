from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Vacancy
from authorization.models import User
from companies.models import Company
from rest_framework.authtoken.models import Token
import datetime
from decimal import *

class VacancyViewSetTests(APITestCase):
    """ Tests for VacancyViewSet class """

    def setUp(self):
        """ Setting up test dependencies """
        self.user = User.objects.create(email="example1@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00)


    def test_success_list_receiving(self):
        """ Test success receiving of the vacancies list """

        url = "/api/v1/companies/{}/vacancies/".format(self.company.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
