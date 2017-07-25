from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CompanySerializer
from .models import Company


# Create your views here.
class CompaniesListViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response({'companies': serializer.data})
