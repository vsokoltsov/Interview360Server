from . import APITestCase, datetime, Interview, InterviewEmployee, EMPLOYEE
import ipdb


class InterviewEmployeeViewTest(APITestCase):
    """ Tests for InterviewEmployee view class """

    fixtures = [
        "skill.yaml",
        "user.yaml",
        "auth_token.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml"
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.interview = Interview.objects.last()
        self.employee = InterviewEmployee.objects.filter(
            interview_id=self.interview.id
        ).last().employee

    def test_success_delete_interview_employee(self):
        """ Test success deletion of the interview employee """

        url = "/api/v1/interviews/{}/employees/{}/".format(
            self.interview.id, self.employee.id, format='json'
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
