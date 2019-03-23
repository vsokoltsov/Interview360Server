from django.test import override_settings
import django.core.mail as mail

from . import (
    TransactionTestCase,
    mock,
    datetime,
    User,
    Token,
    Company,
    ImageFactory,
    ContentType,
    UserFactory,
    CompanyFactory,
    CompanyMemberFactory,
    EmployeeForm,
    CompanyMember,
    SpecialtyFactory
)


class EmployeeFormTest(TransactionTestCase):
    """ Test cases for the EmployeeForm object. """

    def setUp(self):
        """ Set up testing dependencies. """

        self.user = UserFactory()
        self.company = CompanyFactory()
        self.employee1 = UserFactory()
        self.employee2 = UserFactory()
        self.employee3 = UserFactory()
        self.company_member = CompanyMemberFactory(
            user_id=self.user.id, company_id=self.company.id,
            role=CompanyMember.COMPANY_OWNER
        )
        employee_1_json = {
            'email': self.employee1.email,
            'role': CompanyMember.EMPLOYEE
        }
        employee_2_json = {
            'email': self.employee2.email,
            'role': CompanyMember.EMPLOYEE
        }
        employee_3_json = {
            'email': self.employee3.email,
            'role': CompanyMember.HR
        }
        self.params = {
            'company_id': self.company.id,
            'employees': [
                employee_1_json,
                employee_2_json,
                employee_3_json,
            ]
        }

    def test_success_form_validation(self):
        """ Test success EmployeeForm's validation. """

        form = EmployeeForm(
            params=self.params
        )
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test failed EmployeeForm's validation. """

        form = EmployeeForm(
            params={}
        )
        self.assertFalse(form.is_valid())

    def test_failed_validation_empty_email(self):
        """ Test failed validation if one of the emails is not present. """

        self.params['employees'][0]['email'] = None
        form = EmployeeForm(
            params=self.params
        )
        self.assertFalse(form.is_valid())

    def test_failed_validation_empty_role(self):
        """ Test failed validation if one of the roles is not present. """

        self.params['employees'][0].pop('role')
        form = EmployeeForm(
            params=self.params
        )
        self.assertFalse(form.is_valid())

    def test_failed_validation_wrong_email_format(self):
        """ Test failed validation if one of the emails has\
        the wrong format."""

        self.params['employees'][0]['email'] = 'awdawdawd'
        form = EmployeeForm(
            params=self.params
        )
        self.assertFalse(form.is_valid())

    def test_failed_validation_role_does_not_exist(self):
        """ Test failed validation of role does not exist """

        self.params['employees'][0]['role'] = 1000
        form = EmployeeForm(
            params=self.params
        )
        self.assertFalse(form.is_valid())

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_mail_sending(self, user_index):
        """ Test success mail sending after receivng users and the company. """

        form = EmployeeForm(
            params=self.params
        )
        form.submit()
        self.assertEqual(len(mail.outbox), 3)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_user_creation(self, user_index_mock):
        """ Tests success creation of the user if it does not exists. """

        self.params['employees'].append({
            'email': 'example4@mail.com',
            'role': CompanyMember.CANDIDATE
        })
        users_count = User.objects.count()

        form = EmployeeForm(
            params=self.params
        )
        form.submit()
        self.assertEqual(User.objects.count(), users_count + 1)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_token_creation(self, user_index):
        """Test creation of token for the new users."""

        tokens_count = Token.objects.count()
        form = EmployeeForm(
            params=self.params
        )
        form.submit()
        self.assertEqual(Token.objects.count(), tokens_count + 3)

    def test_chosen_user_already_belongs_to_company(self):
        """ Test failed validation if user already belongs to a company. """

        new_user = User.objects.create(email="example4@mail.com")
        CompanyMember.objects.create(
            user_id=new_user.id,
            company_id=self.company.id,
            role=CompanyMember.EMPLOYEE)
        employees = [
            {'email': 'example4@mail.com', 'role': CompanyMember.CANDIDATE},
            {'email': 'example2@mail.com', 'role': CompanyMember.EMPLOYEE},
            {'email': 'example3@mail.com', 'role': CompanyMember.CANDIDATE}
        ]
        form_data = {
            'employees': employees,
            'company_id': self.company.id,
            'role': CompanyMember.EMPLOYEE
        }
        form = EmployeeForm(
            params=form_data
        )
        self.assertFalse(form.submit())

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_user_indexing_after_create(self, user_index):
        """ Test if index was created after the employee's creation. """

        form = EmployeeForm(
            params=self.params
        )
        form.submit()

        self.assertTrue(user_index.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_receiving_of_employees_information(self, user_index):
        """Test presence of 'employees' key after success creation."""

        form = EmployeeForm(
            params=self.params
        )
        form.submit()

        self.assertTrue(len(form.data.get('employees')) > 0)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_creating_already_active_company_member(self, user_index):
        """ Test creating already active company member\
        (User already set a password)."""

        user = User.objects.create(email='test_new@gmail.com')
        user.set_password('password')
        user.save()
        new_company = Company.objects.first()
        CompanyMember.objects.create(
            user_id=user.id, company_id=new_company.id,
            role=CompanyMember.EMPLOYEE, active=True
        )
        form_data = {
            'employees': [
                {
                    'email': user.email,
                    'role': CompanyMember.CANDIDATE
                }
            ],
            'company_id': self.company.id
        }

        form = EmployeeForm(
            params=form_data
        )
        form.submit()
        cm = CompanyMember.objects.last()
        self.assertTrue(cm.active)
