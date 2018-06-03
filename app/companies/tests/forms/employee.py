from . import (mock, TransactionTestCase, Token, EmployeeForm,
               Company, CompanyMember, User, datetime, HR, CANDIDATE,
               override_settings)
import django.core.mail as mail


class EmployeeFormTest(TransactionTestCase):
    """Tests for the EmployeeFormTest class."""

    fixtures = [
        'user.yaml',
        'auth_token.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """Set up test dependencies."""

        self.company = Company.objects.first()
        self.hr = self.company.get_employees_with_role(HR)[0]
        self.user = User.objects.create(email="test@mail.com")
        self.token = Token.objects.create(user=self.user)
        self.company_member = CompanyMember.objects.create(
            user_id=self.user.id, company_id=self.company.id, role=CANDIDATE
        )
        self.form_data = {
            'company_pk': self.company.id,
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }

    def test_success_form_validation(self):
        """Test success form validation with all necessary parameters."""

        form = EmployeeForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """Test failed form validation."""

        form = EmployeeForm({})
        self.assertFalse(form.is_valid())

    def test_failed_password_matching(self):
        """Test failed form validation due to different password."""

        form_data = {
            'company_pk': self.company.id,
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'bbbbbb'
        }

        form = EmployeeForm(form_data)
        self.assertFalse(form.is_valid())

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch.object(User, 'save')
    @mock.patch('django.contrib.auth.models.User')
    def test_saving_user_information(
            self,
            user_class_mock,
            user_save_mock,
            user_index_mock):
        """Test calling save() method on User."""

        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = User(id=1)

        form = EmployeeForm(self.form_data)
        form.submit()
        self.assertTrue(user_save_mock.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_updating_user_password(self, user_index_mock):
        """Test updating user password."""

        form = EmployeeForm(self.form_data)
        form.submit()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.form_data['password']))

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_company_member_updated(self, user_index_mock):
        """Test update of CompanyMember instance 'active' field."""

        form = EmployeeForm(self.form_data)
        form.submit()

        self.company_member.refresh_from_db()
        self.assertTrue(self.company_member.active)

    def test_user_does_not_have_company_member(self):
        """Test validation failure.

        User does not have a company_member instance.
        """

        user = User.objects.create(email="batman@superman.com")
        token = Token.objects.create(user=user)
        form_data = {
            'company_id': self.company.id,
            'token': token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }

        form = EmployeeForm(form_data)
        self.assertFalse(form.submit())

    def test_user_already_activated_in_company(self):
        """Test if user already activated in company."""

        self.company_member.active = True
        self.company_member.save()
        self.company.refresh_from_db()

        form = EmployeeForm(self.form_data)
        self.assertFalse(form.submit())

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_user_already_has_password(self, user_index_mock):
        """Test submit form if user already has a password."""

        form_data = {
            'company_pk': self.company.id,
            'token': self.token.key
        }
        form = EmployeeForm(form_data)
        self.assertTrue(form.submit())
        self.company_member.refresh_from_db()
        self.assertTrue(self.company_member.active)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_company_member_marked_as_active(self, user_index_mock):
        """Test company member.

        Mark as active even if passwords are not present.
        """

        form_data = {
            'company_pk': self.company.id,
            'token': self.token.key
        }
        form = EmployeeForm(form_data)
        form.submit()
        self.company_member.refresh_from_db()
        self.assertTrue(self.company_member.active)

    @mock.patch('profiles.index.UserIndex.store_index')
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_sending_final_confirmation_mail(self, user_index_mock):
        """Test sending confirmation email."""

        form = EmployeeForm(self.form_data)
        form.submit()
        self.assertEqual(len(mail.outbox), 1)
