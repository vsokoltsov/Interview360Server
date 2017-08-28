from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class VacancyViewSet(viewsets.ModelViewSet):
    """ View class for Vacancy """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def create(self, request, company_pk=None):
        """ POST action for creating a new vacancy """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'vacancy': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
