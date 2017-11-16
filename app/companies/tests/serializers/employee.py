from . import (
    TransactionTestCase, serializers, Company, CompanyMember,
    serializers, User, EmployeeSerializer, datetime, mock, User,
    HR, EMPLOYEE, CANDIDATE, Token
)
import django.core.mail as mail
from django.test import override_settings
import ipdb

class EmployeeSerializerTest(TransactionTestCase):
    """ Test employee serializer class """

    fixtures = [
        'user.yaml',
        'company.yaml'
    ]

    def setUp(self):
        """ Test credentials set up """

        self.company = Company.objects.last()
        self.user = self.company.get_employees_with_role(HR)[0]
        self.form_data = {
            'emails': [
                { 'email': 'example1@mail.com', 'role': CANDIDATE},
                { 'email': 'example2@mail.com', 'role': EMPLOYEE},
                { 'email': 'example3@mail.com', 'role': CANDIDATE }
            ],
            'company_id': self.company.id,
            'role': HR
        }

    def test_success_validation(self):
        """ Tests success serializer validation """

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Test failed serializer validation """

        serializer = EmployeeSerializer(data={},
                                        context={'user': self.user})
        self.assertFalse(serializer.is_valid())

    def test_failed_validation_if_role_does_not_exists(self):
        """ Test failed validation if role does not exists """

        self.form_data['role'] = 1000
        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        self.assertFalse(serializer.is_valid())


    def test_success_email_validation(self):
        """ Validation failed if request.user email is in the emails list """

        self.form_data['emails'] = [
            self.user.email,
            'example2@mail.com',
            'example3@mail.com'
        ]

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        self.assertFalse(serializer.is_valid())


    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_mail_sending(self, user_index):
        """ Test success mail sending after receivng users and the company """

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(mail.outbox), 3)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_user_creation(self, user_index_mock):
        """ Tests success creation of the user if it does not exists """

        users_count = User.objects.count()

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(User.objects.count(), users_count + 3)

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_token_creation(self, user_index):
        """ Test creation of token for the new users """

        tokens_count = Token.objects.count()

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertEqual(Token.objects.count(), tokens_count + 3)

    def test_chosen_user_already_belongs_to_company(self):
        """ Test failed validation if user already belongs to a company """

        new_user = User.objects.create(email="example4@mail.com")
        CompanyMember.objects.create(user_id=new_user.id, company_id=self.company.id, role=EMPLOYEE)
        form_data = {
            'emails': [
                'example4@mail.com',
                'example2@mail.com',
                'example3@mail.com'
            ],
            'company_id': self.company.id,
            'role': EMPLOYEE
        }
        serializer = EmployeeSerializer(data=form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        self.assertFalse(serializer.save())


    @mock.patch('profiles.index.UserIndex.store_index')
    def test_user_indexing_after_create(self, user_index):
        """ Test if index was created after the employee's creation """

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertTrue(user_index.called)
