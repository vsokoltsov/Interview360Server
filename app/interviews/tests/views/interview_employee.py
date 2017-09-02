from . import APITestCase, datetime, Interview, InterviewEmployee

class InterviewEmployeeViewTest(APITestCase):
    """ Tests for InterviewEmployee view class """

    fixtures = [
        "roles.yaml",
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
        self.employee = InterviewEmployee.objects.get(
            interview_id=self.interview.id, role_id=4).employee

    def test_success_delete_interview_employee(self):
        """ Test success deletion of the interview employee """

        url = "/api/v1/interviews/{}/employees/{}/".format(
            self.interview.id, self.employee.id
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
