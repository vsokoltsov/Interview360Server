import mock
from django.test import TransactionTestCase
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember, Specialty
from authorization.models import User
from companies.serializers import (
    CompanySerializer, EmployeeSerializer, EmployeesSerializer
)
import datetime
from roles.constants import HR, EMPLOYEE, CANDIDATE

from .employees import EmployeesSerializerTest
