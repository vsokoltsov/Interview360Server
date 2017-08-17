from . import (
    TransactionTestCase, serializers, Company, CompanyMember,
    serializers, User, EmployeeSerializer, datetime, mock, User
)
import django.core.mail as mail
from django.test import override_settings

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
            'company_id': self.company.id
        }

    def test_success_validation(self):
        """ Tests success serializer validation """

        serializer = EmployeeSerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Test failed serializer validation """

        serializer = EmployeeSerializer(data={})
        self.assertFalse(serializer.is_valid())

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    def test_success_mail_sending(self):
        """ Test success mail sending after receivng users and the company """

        serializer = EmployeeSerializer(data=self.form_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(mail.outbox), 3)

    @mock.patch('authorization.models.User.objects.create')
    def test_success_user_creation(self, user_class_mock):
        """ Tests success creation of the user if it does not exists """

        user_class_mock.objects = mock.MagicMock()
        user_class_mock.objects.create = mock.MagicMock()
        user_class_mock.objects.create.return_value = User(id=1)
        serializer = EmployeeSerializer(data=self.form_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(user_class_mock.call_count, 3)

    @mock.patch('rest_framework.authtoken.models.Token.objects.get_or_create')
    def test_success_token_creation(self, token_mock):
        """ Test creation of token for the new users """

        token_mock.user = User(id=1)
        token_mock.return_value = ("12345", 12)

        serializer = EmployeeSerializer(data=self.form_data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(token_mock.call_count, 3)
