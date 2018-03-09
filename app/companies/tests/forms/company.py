from . import (
    TransactionTestCase, mock, datetime, Company,
    UserFactory, CompanyFactory, CompanyMemberFactory, CompanyForm
)
import ipdb

class CompanyFormTest(TransactionTestCase):
    """ Test cases for the company form object """

    def setUp(self):
        """ Setting up testing dependencies """

        self.user = UserFactory()
        self.params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': '2015-02-01',
            'owner_id': self.user.id
        }

    def test_success_form_validation(self):
        """ Test success form validation """

        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test failed form validation """

        form = CompanyForm(
            obj=Company(), params={}, current_user=self.user
        )
        self.assertFalse(form.is_valid())

    def test_failed_form_validation_if_current_user_abscent(self):
        """ Test failed form validation if current user is abscent """

        form = CompanyForm(
            obj=Company(), params={}
        )
        self.assertFalse(form.is_valid())
        self.assertTrue('current_user' in form.errors)

    def test_success_company_creation(self):
        """ Test success creation of the companies """

        companies_count = Company.objects.count()
        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        self.assertEqual(Company.objects.count(), companies_count + 1)

    def test_success_company_update(self):
        """ Test success company update """

        company = CompanyFactory()
        company_member = CompanyMemberFactory(user_id=self.user.id, company_id=company.id)
        form = CompanyForm(
            obj=company, params=self.params, current_user=self.user
        )
        form.submit()
        company.refresh_from_db()
        self.assertEqual(company.name, self.params['name'])

    def test_failed_company_update_user_does_not_belong_to_company(self):
        """ Test failed validation if user does not belongs to company """

        company = CompanyFactory()
        form = CompanyForm(
            obj=company, params=self.params, current_user=self.user
        )
        self.assertFalse(form.submit())
