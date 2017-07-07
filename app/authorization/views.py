from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import RegistrationForm, AuthorizationForm, RestorePasswordForm
from . import models
from .serializers import CurrentUserSerializer
# from serializers import CurrentUserSerializer

import ipdb

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



class CurrentUserView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'current_user': CurrentUserSerializer(request.user).data
        })

class RestorePasswordViewSet(viewsets.ViewSet):

    def create(self, request):
        form = RestorePasswordForm(request.data)

        if form.submit():
            return Response({'message': 'Mail was succesfully sended'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST )
