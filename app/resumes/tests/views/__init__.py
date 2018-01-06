from rest_framework.test import APITestCase
import mock
from rest_framework.authtoken.models import Token
from roles.constants import HR, EMPLOYEE, CANDIDATE
from skills.models import Skill
from companies.models import Company
from resumes.models import Resume

from .resume import ResumeViewTest
