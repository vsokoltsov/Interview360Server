from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from resumes.serializers import ResumesSerializer, ResumeSerializer, ResumesFilter
from rest_framework.decorators import list_route
from resumes.models import Resume, Workplace, Contact
from resumes.forms import ResumeForm
from resumes.index import ResumesIndex
from resumes.search import ResumesSearch
from resumes.query import ResumesQuery
from common.query_parser import QueryParser

from .resumes import ResumeViewSet
from .workplaces import WorkplacesApiView
from .workplaces_delete import WorkplacesDeleteApiView
from .contact import ContactApiView
