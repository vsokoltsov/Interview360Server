from django.test import TransactionTestCase
from roles.constants import HR, EMPLOYEE, CANDIDATE
from resumes.forms import WorkplaceForm, ResumeForm, ContactForm
from skills.models import Skill
from companies.models import Company
from resumes.models import Resume, Workplace, Contact
import mock

from .workplace import WorkplaceFormTest
from .resume import ResumeFormTest
