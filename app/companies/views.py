from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import CompanySerializer
from .models import Company
from .permissions import AllowedToUpdateCompany
import ipdb

# Create your views here.
class CompaniesListViewSet(viewsets.ViewSet):
    """ Viewset for company actions """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, AllowedToUpdateCompany, )

    def list(self, request):
        """ Receive a list of companies """

        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response({'companies': serializer.data})

    def create(self, request):
        """ Creates a new company """

        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'company': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Update an existent company """

        company = get_company(request.user, pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'company': serializer.data},
                        status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Return detail information about company """

        company = self.get_company(request.user, pk)
        serializer = CompanySerializer(company)
        return Response({ 'company': serializer.data })

    def destroy(self, request, pk=None):
        """ Deletes selected company """

        company = self.get_company(request.user, pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_company(user, pk):
        """ Helper method; Receives particular company from the queryset """
        queryset = user.companies.all()
        company = get_object_or_404(queryset, pk=pk)
