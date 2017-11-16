import mock
from django.test import TransactionTestCase
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from companies.models import Company, CompanyMember
from authorization.models import User
from companies.serializers import CompanySerializer, EmployeeSerializer
import datetime
from roles.constants import HR, EMPLOYEE, CANDIDATE

from .company_serializer import CompanySerializerTests
from .employee import EmployeeSerializerTest
