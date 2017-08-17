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

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    def test_success_mail_sending(self):
        """ Test success mail sending after receivng users and the company """

        form_data = {
            'emails': [
                'example!@mail.com',
                'example!@mail.com',
                'example!@mail.com'
            ],
            'company_id': self.company.id
        }
        serializer = EmployeeSerializer(data=form_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(mail.outbox), 3)
