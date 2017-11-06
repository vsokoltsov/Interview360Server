from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Vacancy
from companies.models import Company
from .serializers import VacancySerializer
from common.serializers.base_vacancy_serializer import BaseVacancySerializer
from .permissions import VacancyPermission
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .search import VacancySearch
import ipdb

class VacancyViewSet(viewsets.ModelViewSet):
    """ View class for Vacancy """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, VacancyPermission, )

    def get_queryset(self):
        """ Return queryset for vacancies """

        vacancies = Vacancy.objects.prefetch_related(
            'skills', 'company', 'company__attachments'
        ).filter(company_id=self.kwargs['company_pk'])
        return vacancies

    def get_serializer_class(self):
        """ Return serializer for specific action """

        if self.action == 'list':
            return BaseVacancySerializer
        else:
            return VacancySerializer

    def create(self, request, company_pk=None):
        """ POST action for creating a new vacancy """

        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'vacancy': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, company_pk = None):
        """ PUT action for updating existent vacancy """

        vacancy = get_object_or_404(Vacancy, pk=pk)
        serializer = VacancySerializer(vacancy, data=request.data,
                                           partial=True)
        if serializer.is_valid() and serializer.save():
            return Response({'vacancy': serializer.data},
                             status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                             status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def search(self, request, company_pk=None):
        """ Action for vacancy search """

        query = request.query_params.get('q')
        search = VacancySearch()
        results = search.find(query, company_pk)
        return  Response({ 'vacancies': results })
