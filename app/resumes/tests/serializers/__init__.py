from django.test import TransactionTestCase
from resumes.serializers import ResumeSerializer
from roles.constants import HR, EMPLOYEE, CANDIDATE
from skills.models import Skill
from companies.models import Company
from resumes.models import Resume
import mock

from .resume import ResumeSerializerTest
