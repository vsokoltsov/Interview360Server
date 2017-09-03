from . import (
    TransactionTestCase, serializers, Company, CompanyMember,
    serializers, User, EmployeeSerializer, datetime, mock, User, HR, EMPLOYEE
)
import django.core.mail as mail
from django.test import override_settings
import ipdb

class EmployeeSerializerTest(TransactionTestCase):
    """ Test employee serializer class """

    def setUp(self):
        """ Test credentials set up """

        self.user = User.objects.create(email="example@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.date.today())
        self.form_data = {
            'emails': [
                'example1@mail.com',
                'example2@mail.com',
                'example3@mail.com'
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

        form_data = {
            'emails': [
                'example1@mail.com',
                'example2@mail.com',
                'example3@mail.com'
            ],
            'company_id': self.company.id,
            'role': 10000
        }
        serializer = EmployeeSerializer(data=form_data,
                                        context={'user': self.user})
        self.assertFalse(serializer.is_valid())


    def test_success_email_validation(self):
        """ Validation failed if request.user email is in the emails list """

        self.form_data['emails'] = [
            'example@mail.com',
            'example2@mail.com',
            'example3@mail.com'
        ]

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        self.assertFalse(serializer.is_valid())


    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    def test_success_mail_sending(self):
        """ Test success mail sending after receivng users and the company """

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(mail.outbox), 3)

    @mock.patch('authorization.models.User.objects.create')
    @mock.patch('rest_framework.authtoken.models.Token.objects.get_or_create')
    @mock.patch('companies.models.CompanyMember.objects.create')
    def test_success_user_creation(self, company_member_mock, token_mock, user_class_mock):
        """ Tests success creation of the user if it does not exists """

        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = User(id=1)

        token_mock.user = User(id=1)
        token_mock.objects = mock.MagicMock()
        token_mock.get_or_create = mock.MagicMock()
        token_mock.return_value = ("12345", 12)

        company_member_mock.objects = mock.MagicMock()
        company_member_mock.objects.create = mock.MagicMock()

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(user_class_mock.call_count, 3)

    @mock.patch('rest_framework.authtoken.models.Token.objects.get_or_create')
    def test_success_token_creation(self, token_mock):
        """ Test creation of token for the new users """

        token_mock.user = User(id=1)
        token_mock.return_value = ("12345", 12)

        serializer = EmployeeSerializer(data=self.form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        self.assertEqual(token_mock.call_count, 3)

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
            'role_id': EMPLOYEE
        }
        serializer = EmployeeSerializer(data=form_data,
                                        context={'user': self.user})
        serializer.is_valid()
        self.assertFalse(serializer.save())
