from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Vacancy
from .serializers import VacancySerializer
from .permissions import VacancyPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class VacancyViewSet(viewsets.ModelViewSet):
    """ View class for Vacancy """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, VacancyPermission, )
    serializer_class = VacancySerializer

    def get_queryset(self):
        """ Return queryset for vacancies """

        vacancies = Vacancy.objects.prefetch_related('skills', 'company')
        return vacancies

    def create(self, request, company_pk=None):
        """ POST action for creating a new vacancy """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'vacancy': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, company_pk = None):
        """ PUT action for updating existent vacancy """

        vacancy = get_object_or_404(Vacancy, pk=pk)
        serializer = self.serializer_class(vacancy, data=request.data,
                                           partial=True)
        if serializer.is_valid() and serializer.save():
            return Response({'vacancy': serializer.data},
                             status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                             status=status.HTTP_400_BAD_REQUEST)
