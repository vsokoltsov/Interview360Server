from . import (
    TransactionTestCase, serializers, Company, CompanyMember,
    serializers, User, EmployeeSerializer, datetime, mock
)
import ipdb

class EmployeeSerializerTest(TransactionTestCase):

    def test_success_saving(self):
        form_data = { 'emails': ['example1@mail.com', 'example2@mail.com'], 'company_id': 1}
        serializer = EmployeeSerializer(data=form_data)
        serializer.is_valid()
        serializer.save()
