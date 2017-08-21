from django.shortcuts import render
from rest_framework import viewsets
from .models import Role
from .serializers import RoleSerializer

# Create your views here.
class RolesViewSet(viewsets.ModelViewSet):
    """ Roles ViewSet class """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
