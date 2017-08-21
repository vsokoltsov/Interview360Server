from . import (
    TransactionTestCase, serializers, Company, CompanyMember, Role,
    serializers, User, CompanySerializer, datetime, mock
)

class CompanySerializerTests(TransactionTestCase):
    """ Tests for CompanySerializer class """

    def setUp(self):
        """ Setting up necessary dependencies """

        user = User.objects.create(email="example@mail.com", password="12345678")
        role = Role.objects.create(name='owner')
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.date.today())
        company_member = CompanyMember.objects.create(user_id=user.id,
                                                      company_id=self.company.id,
                                                      role_id=role.id)

        self.company_params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': datetime.date.today(),
            'owner_id': user.id
        }

        self.serializer = CompanySerializer(instance=self.company)

    def test_contains_expected_field(self):
        """ Test presence of serializer expected field """

        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'city',
                                                'description', 'start_date',
                                                'created_at', 'employees']))

    def test_success_validation_of_new_company(self):
        """ Test success case of creation of the new company """

        serializer = CompanySerializer(data=self.company_params)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation_of_new_company(self):
        """ Test failed case of creation of the new company """

        serializer = CompanySerializer(data={})
        self.assertFalse(serializer.is_valid())

    @mock.patch('companies.models.Company.objects.create')
    def test_success_company_creation(self, company_class_mock):
        """ Test success case of saving new Company """

        test_company = Company(id=1)
        company_class_mock.objects = mock.MagicMock()
        company_class_mock.objects.create = mock.MagicMock()
        company_class_mock.objects.create.return_value = test_company

        serializer = CompanySerializer(data=self.company_params)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(company_class_mock.called)

    @mock.patch('companies.models.CompanyMember.objects.create')
    def test_success_company_member_creation(self, company_member_mock):
        """ Test that CompanyMember objects was created just after the Company """

        test_company_member = CompanyMember(1)

        company_member_mock.objects = mock.MagicMock()
        company_member_mock.objects.create = mock.MagicMock()
        company_member_mock.objects.create.return_value = test_company_member

        serializer = CompanySerializer(data=self.company_params)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(company_member_mock.called)

    def test_success_company_update(self):
        """ Test success company updated operation """

        serializer = CompanySerializer(self.company, data=self.company_params)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.company.name, self.company_params['name'])

    def test_validation_user_existance(self):
        """ Test raising error if user is abscent """

        params = {
            'name': 'NAME',
            'city': 'City',
            'start_date': datetime.date.today(),
            'owner_id': 15
        }

        serializer = CompanySerializer(data=params)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('owner_id' in serializer.errors)
