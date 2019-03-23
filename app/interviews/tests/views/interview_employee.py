from . import (
    APITestCase, datetime, Interview, InterviewEmployee, EMPLOYEE, CANDIDATE,
    Company, Token
)
import ipdb


class InterviewEmployeeViewTest(APITestCase):
    """Tests for InterviewEmployee view class."""

    fixtures = [
        "skill.yaml",
        "user.yaml",
        "auth_token.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml"
    ]

    def setUp(self):
        """Set up test dependencies."""

        self.company = Company.objects.first()
        self.candidate = self.company.get_employees_with_role(CANDIDATE)[-1]
        self.interview = Interview.objects.last()
        self.employee = InterviewEmployee.objects.filter(
            interview_id=self.interview.id
        ).last().employee
        self.token = Token.objects.get(user=self.candidate)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_success_delete_interview_employee(self):
        """Test success deletion of the interview employee."""

        url = "/api/v1/interviews/{}/employees/{}/".format(
            self.interview.id, self.employee.id, format='json'
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
