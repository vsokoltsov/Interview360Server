from django.test import TransactionTestCase
from roles.constants import HR, EMPLOYEE, CANDIDATE
from resumes.forms import WorkplaceForm
from skills.models import Skill
from companies.models import Company
from resumes.models import Resume, Workplace
import mock

from .workplace import WorkplaceFormTest
