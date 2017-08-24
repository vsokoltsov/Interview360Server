from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Vacancy
from authorization.models import User
from companies.models import Company
from rest_framework.authtoken.models import Token
import datetime
from decimal import *
import ipdb

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
        self.url = "/api/v1/companies/{}/vacancies/".format(self.company.id)
        self.form_data = {
            'title': 'Test',
            'description': 'Test',
            'salary': '150.00',
            'company': self.company.id
        }


    def test_success_list_receiving(self):
        """ Test success receiving of the vacancies list """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_success_vacancy_creation(self):
        """ Test success company creation """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)

    def test_failed_vacancy_creation(self):
        """ Test failed creation of the vacancy """

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_success_vacancy_update(self):
        """ Test success update of the vacancy """

        response = self.client.put(
            self.url + "{}/".format(self.vacancy.id),
            self.form_data
        )
        self.assertEqual(response.status_code, 200)

    def test_failed_vacancy_update(self):
        """ Test failed update of the vacancy """

        response = self.client.put(
            self.url + "{}/".format(self.vacancy.id),
            {}
        )
        self.assertEqual(response.status_code, 400)

    def test_success_delete_vacancy(self):
        """ Test success vacancy deletion """

        response = self.client.delete(self.url + "{}/".format(self.vacancy.id))
        self.assertEqual(response.status_code, 204)
