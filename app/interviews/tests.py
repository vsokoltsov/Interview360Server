from django.test import TestCase, TransactionTestCase
from .serializers import InterviewSerializer
from authorization.models import User
from companies.models import Company, CompanyMember
from vacancies.models import Vacancy
from skills.models import Skill
from roles.models import Role
import datetime
import ipdb
# Create your tests here.

class InterviewSerializerTests(TransactionTestCase):
    """ Tests for InterviewSerializer serializer """

    def setUp(self):
        """ Setting up test dependencies """

        self.owner = User.objects.create(email="example1@mail.com")
        self.hr = User.objects.create(email="example2@mail.com")
        self.candidate = User.objects.create(email="example3@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        self.role = Role.objects.create(name='CEO')
        self.hr_role = Role.objects.create(name='HR')
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.owner.id,
            role_id=self.hr_role.id
        )
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.hr.id,
            role_id=self.role.id
        )
        self.skill = Skill.objects.create(name="Computer Science")
        self.vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00)
        self.vacancy.skills.set([self.skill.id])
        self.form_data = {
            'candidate': self.candidate.id,
            'vacancy': self.vacancy.id,
            'interviewees': [
                self.hr.id
            ],
            'assigned_at': datetime.datetime.now()
        }

    def test_succes_validation(self):
        """ Test that serializer's validation is passed """

        serializer = InterviewSerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Test that serializer's validation is failed """

        serializer = InterviewSerializer(data={})
        self.assertFalse(serializer.is_valid())
