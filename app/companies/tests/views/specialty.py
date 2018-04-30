from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime, EMPLOYEE,
    CompanyFactory, CompanyMemberFactory, UserFactory, mock
)


class SpecialtiesSearchViewTest(APITestCase):
    """ Tests for SpecialtiesSearchView """

    def setUp(self):
        """ Setting up test dependencies """

        self.company = CompanyFactory()
        self.user = UserFactory()
        company_member = CompanyMemberFactory(
            company_id=self.company.id, user_id=self.user.id, role=EMPLOYEE
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @mock.patch('companies.search.SpecialtySearch.find')
    def test_search_action(self, search_mock):
        """ Test success search of specialty """

        specialty_index = [
            {'id': 1},
            {'id': 2},
            {'id': 3}
        ]
        search_mock.return_value = specialty_index
        url = "/api/v1/companies/specialties/search/?q={}".format(
            'buzzword'
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['specialties'], specialty_index)
