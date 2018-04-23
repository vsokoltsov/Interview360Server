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
from companies.search import CompanySearch, SpecialtySearch
from companies.forms import CompanyForm
from companies.query import CompaniesQuery
from common.query_parser import QueryParser
from common.services.cities_service import CitiesService

from companies.serializers import (
    CompanySerializer, EmployeeSerializer,
    CompaniesSerializer, EmployeesSerializer, CompaniesFilter,
    SpecialtiesSerializer
)
from companies.models import Company, CompanyMember, Specialty
from authorization.models import User
from companies.permissions import CompanyPermissions, EmployeePermission
from companies.forms import EmployeeForm

from .company import CompaniesViewSet
from .employee import EmployeesViewSet
from .employee_activation import EmployeeActivationView
from .specialties import SpecialtiesSearchView
