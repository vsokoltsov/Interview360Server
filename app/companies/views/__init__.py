from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from companies.serializers import CompanySerializer, EmployeeSerializer
from companies.models import Company
from authorization.models import User
from companies.permissions import AllowedToUpdateCompany

from .company import CompaniesViewSet
from .employee import EmployeesViewSet
