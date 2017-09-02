from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase
from .serializers import InterviewSerializer
from .models import Interview, InterviewEmployee
from authorization.models import User
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember
from vacancies.models import Vacancy
from skills.models import Skill
from roles.models import Role
import datetime
import mock
import ipdb
from .views import InterviewViewSet, InterviewEmployeeView
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
            company_id=self.company.id, salary=120.00
        )
        self.vacancy.skills.set([self.skill.id])
        date = datetime.datetime.now() + datetime.timedelta(days=10)
        self.form_data = {
            'candidate_id': self.candidate.id,
            'vacancy_id': self.vacancy.id,
            'interviewees': [
                self.hr.id
            ],
            'assigned_at': date
        }
        self.interview = Interview.objects.create(
            candidate_id=self.form_data['candidate_id'],
            vacancy_id=self.form_data['vacancy_id'],
            assigned_at=date
        )

    def test_succes_validation(self):
        """ Test that serializer's validation is passed """

        serializer = InterviewSerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Test that serializer's validation is failed """

        serializer = InterviewSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_failed_validation_vacancy_is_abscent(self):
        """ Test that serializer's validation failed if vacancy does not exists """

        self.form_data['vacancy_id'] = 100
        serializer = InterviewSerializer(data=self.form_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('vacancy_id' in serializer.errors)

    def test_failed_validation_vacancy_is_unactive(self):
        """ Test that serializer's validation failed is vacancy is not active """

        vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00, active=False
        )
        self.form_data['vacancy_id'] = vacancy.id
        serializer = InterviewSerializer(data=self.form_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('vacancy_id' in serializer.errors)

    def test_failed_validation_if_candidate_does_not_exists(self):
        """ Test that serializer's validation failed if candidate is empty """

        self.form_data['candidate_id'] = 123124124

        serializer = InterviewSerializer(data=self.form_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('candidate_id' in serializer.errors)

    def test_failed_validation_if_assigned_at_less_than_current_date(self):
        """ Test that serializer's validation failed if assigned_at is
            less than current time """

        date = datetime.datetime.now() + datetime.timedelta(days=-10)
        self.form_data['assigned_at'] = date

        serializer = InterviewSerializer(data=self.form_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('assigned_at' in serializer.errors)

    @mock.patch('interviews.models.Interview.objects.create')
    @mock.patch('interviews.models.InterviewEmployee.objects.create')
    def test_success_interview_creation(self, inteview_employee_class_mock, inteview_class_mock):
        """ Test success creation of the interview """

        inteview_employee_class_mock.objects = mock.MagicMock()
        inteview_employee_class_mock.objects.create = mock.MagicMock()
        inteview_employee_class_mock.objects.create.return_value = InterviewEmployee(id=1)

        inteview_class_mock.objects = mock.MagicMock()
        inteview_class_mock.objects.create = mock.MagicMock()
        inteview_class_mock.objects.create.return_value = Interview(id=1)

        serializer = InterviewSerializer(data=self.form_data)
        serializer.is_valid()

        serializer.save()
        self.assertTrue(inteview_class_mock.called)

    @mock.patch('interviews.models.InterviewEmployee.objects.create')
    def test_success_interview_employee_creation(self, inteview_employee_class_mock):
        """ Test success creation of InterviewEmployee instance """

        inteview_employee_class_mock.objects = mock.MagicMock()
        inteview_employee_class_mock.objects.create = mock.MagicMock()
        inteview_employee_class_mock.objects.create.return_value = InterviewEmployee(id=1)

        serializer = InterviewSerializer(data=self.form_data)
        serializer.is_valid()

        serializer.save()
        self.assertTrue(inteview_employee_class_mock.called)
        self.assertTrue(inteview_employee_class_mock.call_count, 1)

    def test_failed_interview_employee_creation(self):
        """ Test failed creation of Interviewemployee for the abscent user """

        self.form_data['interviewees'] = 100

        serializer = InterviewSerializer(data=self.form_data)

        self.assertFalse(serializer.is_valid())
        self.assertTrue('interviewees' in serializer.errors)

    def test_success_update_of_the_interview(self):
        """ Test success updating of the interview instance """

        date = datetime.datetime.now() + datetime.timedelta(days=31)
        date = date.replace(second=0, microsecond=0)
        self.form_data['assigned_at'] = date

        serializer = InterviewSerializer(
            self.interview, data=self.form_data, partial=True
        )
        serializer.is_valid()
        interview = serializer.save()

        self.assertEqual(interview.assigned_at.replace(
            second=0, microsecond=0, tzinfo=None), date
        )

class InterviewViewSetTests(APITestCase):
    """ Tests for InterviewViewSet class """

    def setUp(self):
        """ Setting up test dependencies """

        self.owner = User.objects.create(email="example1@mail.com")
        self.hr = User.objects.create(email="example2@mail.com")
        self.token = Token.objects.create(user=self.hr)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.candidate = User.objects.create(email="example3@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        self.role = Role.objects.create(name='CEO')
        self.hr_role = Role.objects.create(name='HR')
        self.candidate_role = Role.objects.create(name='Candidate')
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.owner.id,
            role_id=self.hr_role.id
        )
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.hr.id,
            role_id=self.role.id
        )
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.candidate.id,
            role_id=self.candidate_role.id
        )
        self.skill = Skill.objects.create(name="Computer Science")
        self.vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00
        )
        self.vacancy.skills.set([self.skill.id])
        date = datetime.datetime.now() + datetime.timedelta(days=10)
        self.form_data = {
            'candidate_id': self.candidate.id,
            'vacancy_id': self.vacancy.id,
            'interviewees': [
                self.hr.id
            ],
            'assigned_at': date
        }
        self.interview = Interview.objects.create(
            candidate_id=self.form_data['candidate_id'],
            vacancy_id=self.form_data['vacancy_id'],
            assigned_at=date
        )
        self.interview_employee = InterviewEmployee.objects.create(
            interview_id=self.interview.id, employee_id=self.hr.id,
            role_id=self.hr_role.id
        )
        self.url = "/api/v1/companies/{}/vacancies/{}/interviews/".format(
            self.company.id, self.vacancy.id
        )

    def test_success_list_receiving(self):
        """ Test success receiving list of the interviews """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_success_interview_creation(self):
        """ Test success creation of the interview """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('interview' in response.data)

    def test_failed_interview_creation(self):
        """ Test failed creation of the interview """

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_success_interview_update(self):
        """ Test success Interview's instance update """

        response = self.client.put(
            self.url + "{}/".format(self.interview.id), self.form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('interview' in response.data)

    def test_success_interview_delete(self):
        """ Test success Interview's instance delete """

        response = self.client.delete(
            self.url + "{}/".format(self.interview.id)
        )
        self.assertEqual(response.status_code, 204)

class InterviewEmployeeTest(APITestCase):
    """ Tests for InterviewEmployee view class """

    def setUp(self):
        """ Setting up test dependencies """

        self.owner = User.objects.create(email="example1@mail.com")
        self.hr = User.objects.create(email="example2@mail.com")
        self.token = Token.objects.create(user=self.hr)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.candidate = User.objects.create(email="example3@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.datetime.now())
        self.role = Role.objects.create(name='CEO')
        self.hr_role = Role.objects.create(name='HR')
        self.candidate_role = Role.objects.create(name='Candidate')
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.owner.id,
            role_id=self.hr_role.id
        )
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.hr.id,
            role_id=self.role.id
        )
        self.company_member = CompanyMember.objects.create(
            company_id=self.company.id, user_id=self.candidate.id,
            role_id=self.candidate_role.id
        )
        self.skill = Skill.objects.create(name="Computer Science")
        self.vacancy = Vacancy.objects.create(
            title="Vacancy name", description="Description",
            company_id=self.company.id, salary=120.00
        )
        self.vacancy.skills.set([self.skill.id])
        date = datetime.datetime.now() + datetime.timedelta(days=10)
        self.form_data = {
            'candidate_id': self.candidate.id,
            'vacancy_id': self.vacancy.id,
            'interviewees': [
                self.hr.id
            ],
            'assigned_at': date
        }
        self.interview = Interview.objects.create(
            candidate_id=self.form_data['candidate_id'],
            vacancy_id=self.form_data['vacancy_id'],
            assigned_at=date
        )
        self.interview_employee_1 = InterviewEmployee.objects.create(
            interview_id=self.interview.id, employee_id=self.hr.id,
            role_id=self.hr_role.id
        )
        self.interview_employee_2 = InterviewEmployee.objects.create(
            interview_id=self.interview.id, employee_id=self.owner.id,
            role_id=self.role.id
        )
        self.url = "/api/v1/companies/{}/vacancies/{}/interviews/".format(
            self.company.id, self.vacancy.id
        )

    def test_success_delete_interview_employee(self):
        """ Test success deletion of the interview employee """
        url = "/api/v1/interviews/{}/employees/{}/".format(
            self.interview.id, self.owner.id
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
