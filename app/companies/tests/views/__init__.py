from rest_framework.test import APITestCase
import mock
from django.core.files.storage import FileSystemStorage
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember
from authorization.models import User
import datetime
from roles.constants import COMPANY_OWNER, HR, EMPLOYEE, CANDIDATE
from companies.index import CompanyIndex

from .company import CompaniesViewSetTests
from .employee import EmployeesViewSetTests
from .employee_activation import EmployeeActivationTests
