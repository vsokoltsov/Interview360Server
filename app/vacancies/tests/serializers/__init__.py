from django.test import TransactionTestCase
from vacancies.models import Vacancy
from authorization.models import User
from companies.models import Company
from rest_framework.authtoken.models import Token
from skills.models import Skill
import datetime
from vacancies.serializers import VacancySerializer
import mock

from .vacancy import VacancySerializerTest
