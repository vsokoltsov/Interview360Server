from feedbacks.views import FeedbackViewSet
from rest_framework.test import APITestCase
from feedbacks.models import Feedback
from interviews.models import Interview
from roles.constants import HR, EMPLOYEE, CANDIDATE
from companies.models import Company
from rest_framework.authtoken.models import Token

from .feedback import FeedbackViewSetTest
