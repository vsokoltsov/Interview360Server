from . import (
    APITestCase, Vacancy, User, Company, CompanyMember, HR, Token, Skill,
    datetime, mock
)
from vacancies.index import VacancyIndex

class VacancyViewSetTests(APITestCase):
    """ Tests for VacancyViewSet class """

    fixtures = [
        'skill.yaml',
        'user.yaml',
        'auth_token.yaml',
        'company.yaml',
        'vacancy.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(HR)[0]
        self.token = Token.objects.get(user=self.user)
        self.skill = Skill.objects.first()
        self.vacancy = Vacancy.objects.filter(company_id=self.company.id).first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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
        self.assertEqual(len(response.data), 2)

    def test_success_retrieve_action(self):
        """ Success receivinf of the detail vacancy information """

        response = self.client.get(self.url + "{}/".format(self.vacancy.id))
        self.assertEqual(response.status_code, 200)

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_success_vacancy_creation(self, vacancy_index_mock):
        """ Test success vacancy creation """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual('vacancy' in response.data, True)

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_failed_vacancy_creation(self, vacancy_index_mock):
        """ Test failed creation of the vacancy """

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_success_vacancy_update(self, vacancy_index_mock):
        """ Test success update of the vacancy """

        response = self.client.put(
            self.url + "{}/".format(self.vacancy.id),
            self.form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vacancy' in response.data)

    @mock.patch.object(VacancyIndex, 'get')
    @mock.patch.object(VacancyIndex, 'delete')
    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_success_delete_vacancy(self, vacancy_index_mock, vacancy_delete, vacancy_save):
        """ Test success vacancy deletion """

        response = self.client.delete(self.url + "{}/".format(self.vacancy.id))
        self.assertEqual(response.status_code, 204)
