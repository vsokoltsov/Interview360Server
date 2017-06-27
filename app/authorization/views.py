from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status

from .forms import RegistrationForm
from . import models

class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request):
        form = RegistrationForm(request.data)
        if form.is_valid():
            token = form.submit()
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST )
