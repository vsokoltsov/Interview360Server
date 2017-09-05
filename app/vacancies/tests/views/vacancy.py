from . import (
    APITestCase, Vacancy, User, Company, CompanyMember, HR, Token, Skill, datetime
)

class VacancyViewSetTests(APITestCase):
    """ Tests for VacancyViewSet class """

    def setUp(self):
        """ Setting up test dependencies """

        self.user = User.objects.create(email="example1@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.user.id, role=HR
        )
        self.token = Token.objects.create(user=self.user)
        self.skill = Skill.objects.create(name="Computer Science")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00)
        self.url = "/api/v1/companies/{}/vacancies/".format(self.company.id)
        self.form_data = {
            'title': 'Test',
            'description': 'Test',
            'salary': '150.00',
            'company_id': self.company.id,
            'skills': [
                self.skill.id
            ]
        }

    def test_success_list_receiving(self):
        """ Test success receiving of the vacancies list """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_success_retrieve_action(self):
        """ Success receivinf of the detail vacancy information """

        response = self.client.get(self.url + "{}/".format(self.vacancy.id))
        self.assertEqual(response.status_code, 200)

    def test_success_vacancy_creation(self):
        """ Test success vacancy creation """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual('vacancy' in response.data, True)

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
        self.assertTrue('vacancy' in response.data)

    def test_success_delete_vacancy(self):
        """ Test success vacancy deletion """

        response = self.client.delete(self.url + "{}/".format(self.vacancy.id))
        self.assertEqual(response.status_code, 204)
