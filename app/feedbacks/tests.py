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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_success_receiving_feedbacks_list(self):
        """ Test success receiving of the feedbacks list """
        response = self.client.get('/api/v1/feedbacks/')
        self.assertEqual(response.status_code, 200)
