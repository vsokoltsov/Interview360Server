from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status

from .forms import RegistrationForm, AuthorizationForm
from . import models

class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request):
        form = RegistrationForm(request.data)
        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST )

class AuthorizationViewSet(viewsets.ViewSet):

    def create(self, request):
        form = AuthorizationForm(request.data)
        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST )
