from django.test import TestCase
from .views import FeedbackViewSet
from rest_framework.test import APITestCase
from .models import Feedback
from interviews.models import Interview
from roles.constants import HR, EMPLOYEE, CANDIDATE
from companies.models import Company
from rest_framework.authtoken.models import Token
# Create your tests here.

class FeedbackViewSetTest(APITestCase):
    """ Tests for the FeedbackViewSet """

    fixtures = [
        "skill.yaml",
        "user.yaml",
        "auth_token.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml",
        "feedback.yaml"
    ]

    def setUp(self):
        """ Setting up test depencencies """
        self.company = Company.objects.first()
        self.hr = self.company.get_employees_with_role(HR)[-1]
        self.token = Token.objects.get(user=self.hr)
        self.feedback = Feedback.objects.last()
        self.interview = Interview.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = '/api/v1/feedbacks/'
        self.form_data = {
            'user': self.hr.id,
            'description': 'AAA',
            'object_id': self.interview.id,
            'content_type': 'interviews.interview'
        }

    def test_success_receiving_feedbacks_list(self):
        """ Test success receiving of the feedbacks list """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_retrieving_action(self):
        """ Test success receiving ofthe detail information about feedback """

        response = self.client.get(self.url + "{}/".format(self.feedback.id))
        self.assertEqual(response.status_code, 200)

    def test_success_create_action(self):
        """ Test success creation of the feedback """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)

    def test_failed_create_action(self):
        """ Test success creation of the feedback """

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_success_update_action(self):
        """ Test success update of the feedback """

        response = self.client.get(
            self.url + "{}/".format(self.feedback.id), self.form_data
        )
        self.assertEqual(response.status_code, 200)

    def test_success_destroy_action(self):
        """ Test success delete action """

        response = self.client.delete(self.url + "{}/".format(self.feedback.id))
        self.assertEqual(response.status_code, 204)
