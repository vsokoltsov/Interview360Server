from django.test import TestCase

from companies.query import CompaniesQuery

from companies.models import Company, CompanyMember
from authorization.factory import UserFactory
from companies.factory import CompanyFactory, CompanyMemberFactory


class CompaniesQueryTest(TestCase):
    """Tests for the CompaniesQuery class."""

    def setUp(self):
        """Set up testing dependencies."""

        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.user_3 = UserFactory()
        self.user_4 = UserFactory()

        self.company_1 = CompanyFactory()
        self.company_2 = CompanyFactory()
        self.company_3 = CompanyFactory()
        self.company_4 = CompanyFactory()

        self.company_member_1 = CompanyMemberFactory(
            user_id=self.user_1.id, company_id=self.company_1.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_3 = CompanyMemberFactory(
            user_id=self.user_1.id, company_id=self.company_2.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_4 = CompanyMemberFactory(
            user_id=self.user_1.id, company_id=self.company_3.id,
            role=CompanyMember.EMPLOYEE
        )
        self.company_member_5 = CompanyMemberFactory(
            user_id=self.user_1.id, company_id=self.company_4.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_6 = CompanyMemberFactory(
            user_id=self.user_2.id, company_id=self.company_3.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_7 = CompanyMemberFactory(
            user_id=self.user_3.id, company_id=self.company_1.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_8 = CompanyMemberFactory(
            user_id=self.user_3.id, company_id=self.company_2.id,
            role=CompanyMember.COMPANY_OWNER
        )
        self.company_member_8 = CompanyMemberFactory(
            user_id=self.user_2.id, company_id=self.company_2.id,
            role=CompanyMember.HR
        )
        self.company_member_9 = CompanyMemberFactory(
            user_id=self.user_4.id, company_id=self.company_2.id,
            role=CompanyMember.EMPLOYEE
        )

    def test_receiving_of_companies_list(self):
        """Test of receiving of the companies list."""

        query = CompaniesQuery({}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_3.id, self.company_4.id]
        )

    def test_setting_of_order(self):
        """Test receiving of the companies in particular order."""

        query = CompaniesQuery({'order': 'employees__count'}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_4.id, self.company_1.id,
             self.company_3.id, self.company_2.id]
        )

    def test_reverse_order_value(self):
        """Test receiving of companies with reversed order value."""

        query = CompaniesQuery({'order': '-employees__count'}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_2.id, self.company_1.id,
             self.company_3.id, self.company_4.id]
        )

    def test_receiving_of_wrong_order(self):
        """Test receiving companies in case of the wrong order value."""

        query = CompaniesQuery({'order': 'title'}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_3.id, self.company_4.id]
        )

    def test_empty_order_value(self):
        """Test of receiving empty order value."""

        query = CompaniesQuery({'order': None}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_3.id, self.company_4.id]
        )

    def test_setting_of_role(self):
        """Test receiving of companies for the role of current user."""

        query = CompaniesQuery(
            {'role': CompanyMember.COMPANY_OWNER}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_4.id]
        )

    def test_receiving_of_wrong_role(self):
        """Test receiving of companies list if role is wrong."""

        query = CompaniesQuery({'role': 10}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_3.id, self.company_4.id]
        )

    def test_receiving_of_empty_role(self):
        """Test receiving of companies list if role is None."""

        query = CompaniesQuery({'role': None}, self.user_1)
        response = query.list()
        self.assertEqual(
            [item.id for item in response],
            [self.company_1.id, self.company_2.id,
             self.company_3.id, self.company_4.id]
        )
