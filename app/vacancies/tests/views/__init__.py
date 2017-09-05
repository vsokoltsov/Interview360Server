from rest_framework.test import APITestCase
from vacancies.models import Vacancy
from authorization.models import User
from companies.models import Company, CompanyMember
from rest_framework.authtoken.models import Token
from skills.models import Skill
import datetime
from decimal import *
import mock
from roles.constants import HR

from .vacancy import VacancyViewSetTests
