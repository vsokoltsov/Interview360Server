from . import (
    TransactionTestCase, mock, datetime, Company, ImageFactory, ContentType,
    UserFactory, CompanyFactory, CompanyMemberFactory, CompanyForm, CompanyMember
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
            obj=Company(), params=self.params
        )
        self.assertFalse(form.is_valid())
        self.assertTrue('current_user' in form.errors)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_company_creation(self, user_index, company_index):
        """ Test success creation of the companies """

        companies_count = Company.objects.count()
        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        self.assertEqual(Company.objects.count(), companies_count + 1)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_company_member_creation(self, user_index, company_index):
        """ Test success company member creation along with new company """

        company_members_count = CompanyMember.objects.count()
        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        self.assertEqual(CompanyMember.objects.count(), company_members_count + 1)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_company_update(self, user_index, company_index):
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

    def test_failed_company_update_user_does_not_have_appropriate_role(self):
        """ Test failed validation if user does not"""\
        """ have appropriate role in company """

        company = CompanyFactory()
        company_member = CompanyMemberFactory(
            user_id=self.user.id, company_id=company.id, role=CompanyMember.EMPLOYEE
        )
        form = CompanyForm(
            obj=company, params=self.params, current_user=self.user
        )
        self.assertFalse(form.submit())

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_image_setting(self, user_index, company_index):
        """ Test whether or not image setting came succesfullty """

        attachment = ImageFactory(
            content_type=ContentType.objects.get_for_model(Company)
        )
        self.params['attachment'] = { 'id': attachment.id }
        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        attachment.refresh_from_db()
        self.assertEqual(attachment.object_id, Company.objects.last().id)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_user_index_call(self, user_index, company_index):
        """ Test of the storing of the user's index data """

        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        self.assertTrue(user_index.called)

    @mock.patch('companies.index.CompanyIndex.store_index')
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_company_index_call(self, user_index, company_index):
        """ Test of the storing of the company's index data """

        form = CompanyForm(
            obj=Company(), params=self.params, current_user=self.user
        )
        form.submit()
        self.assertTrue(company_index.called)
