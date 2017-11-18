from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count
from rest_framework.decorators import detail_route, list_route
from profiles.search import UsersSearch
from profiles.index import UserIndex
from companies.index import CompanyIndex
from rest_framework.decorators import list_route
from companies.search import CompanySearch

from companies.serializers import (
    CompanySerializer, EmployeeSerializer, CompaniesSerializer, EmployeesSerializer
)
from companies.models import Company, CompanyMember
from authorization.models import User
from companies.permissions import CompanyPermissions, EmployeePermission
from companies.forms import EmployeeForm

from .company import CompaniesViewSet
from .employee import EmployeesViewSet
from .employee_activation import EmployeeActivationView
