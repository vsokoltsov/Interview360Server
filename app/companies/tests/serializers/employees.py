from . import (
    TransactionTestCase, serializers, Company, CompanyMember,
    serializers, User, EmployeesSerializer, datetime, mock, User,
    HR, EMPLOYEE, CANDIDATE, Token
)
import django.core.mail as mail
from django.test import override_settings
import ipdb


class EmployeesSerializerTest(TransactionTestCase):
    """ EmployeesSerializer class tests """

    fixtures = [
        'user.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """ Test credentials set up """

        self.company = Company.objects.last()
        self.user = self.company.get_employees_with_role(HR)[0]
        self.form_data = {
            'employees': [
                {'email': 'example1@mail.com', 'role': CANDIDATE},
                {'email': 'example2@mail.com', 'role': EMPLOYEE},
                {'email': 'example3@mail.com', 'role': CANDIDATE}
            ],
            'company_id': self.company.id
        }

    def test_success_validation(self):
        """ Tests success serializer validation """

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Tests success serializer validation """

        serializer = EmployeesSerializer(data={},
                                         context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_failed_validation_if_one_of_emails_is_abscent(self):
        """ Test failed validation of one of the emplyee's emails is abscent """

        self.form_data['employees'][0]['email'] = None

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_failed_validation_if_one_of_roles_is_abscent(self):
        """ Test failed validation of one of the emplyee's roles is abscent """

        self.form_data['employees'][0]['role'] = ''

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_failed_validation_if_role_does_not_exists(self):
        """ Test failed validation if role does not exists """

        self.form_data['employees'][0]['role'] = 1000
        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_success_email_validation(self):
        """ Validation failed if request.user email is in the emails list """

        self.form_data['employees'] = [
            {'email': self.user.email, 'role': CANDIDATE},
            {'email': 'example2@mail.com', 'role': EMPLOYEE},
            {'email': 'example3@mail.com', 'role': CANDIDATE}
        ]

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_mail_sending(self, user_index):
        """ Test success mail sending after receivng users and the company """

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(mail.outbox), 3)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_user_creation(self, user_index_mock):
        """ Tests success creation of the user if it does not exists """

        users_count = User.objects.count()

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(User.objects.count(), users_count + 3)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_token_creation(self, user_index):
        """ Test creation of token for the new users """

        tokens_count = Token.objects.count()
        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertEqual(Token.objects.count(), tokens_count + 3)

    def test_chosen_user_already_belongs_to_company(self):
        """ Test failed validation if user already belongs to a company """

        new_user = User.objects.create(email="example4@mail.com")
        CompanyMember.objects.create(
            user_id=new_user.id,
            company_id=self.company.id,
            role=EMPLOYEE)
        form_data = {
            'employees': [
                {'email': 'example4@mail.com', 'role': CANDIDATE},
                {'email': 'example2@mail.com', 'role': EMPLOYEE},
                {'email': 'example3@mail.com', 'role': CANDIDATE}
            ],
            'company_id': self.company.id,
            'role': EMPLOYEE
        }
        serializer = EmployeesSerializer(data=form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        self.assertFalse(serializer.save())

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_user_indexing_after_create(self, user_index):
        """ Test if index was created after the employee's creation """

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertTrue(user_index.called)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_receiving_of_employees_information(self, user_index):
        """ Test presence of 'employees' key after success creation """

        serializer = EmployeesSerializer(data=self.form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertTrue('employees' in serializer.data)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_creating_already_active_company_member(self, user_index):
        """ Test creating already active company member if user
        already set a password """

        user = User.objects.create(email='test_new@gmail.com')
        user.set_password('password')
        user.save()
        new_company = Company.objects.first()
        CompanyMember.objects.create(
            user_id=user.id, company_id=new_company.id, role=EMPLOYEE,
            active=True
        )
        form_data = {
            'employees': [
                {'email': user.email, 'role': CANDIDATE}
            ],
            'company_id': self.company.id
        }

        serializer = EmployeesSerializer(data=form_data,
                                         context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        cm = CompanyMember.objects.last()
        assert cm.active, True
