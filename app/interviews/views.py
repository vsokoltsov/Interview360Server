from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InterviewSerializer
from companies.models import Company
from vacancies.models import Vacancy
import ipdb

class InterviewViewSet(viewsets.ModelViewSet):
    """ View class for Interviews """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = InterviewSerializer

    def get_queryset(self):
        """
        Return scope of interviews where current user is participated
        """
        params = self.kwargs
        company = get_object_or_404(Company, pk=params['company_pk'])
        vacancy = get_object_or_404(Vacancy, pk=params['vacancy_pk'])
        queryset = vacancy.interview_set.all()
        return queryset
