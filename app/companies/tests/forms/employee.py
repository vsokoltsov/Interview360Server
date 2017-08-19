from . import (mock, TransactionTestCase, Token, EmployeeForm,
               Company, CompanyMember, User, datetime)
import ipdb

class EmployeeFormTest(TransactionTestCase):
    """ Tests for the EmployeeFormTest class """

    def setUp(self):
        """ Set up test dependencies """

        self.user = User.objects.create(email="example@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.date.today())
        self.token = Token.objects.create(user=self.user)

        self.form_data = {
            'company_id': self.company.id,
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }

    def test_success_form_validation(self):
        """ Test success form validation with all necessary parameters """

        form = EmployeeForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_failed_form_validation(self):
        """ Test failed form validation """

        form = EmployeeForm({})
        self.assertFalse(form.is_valid())
