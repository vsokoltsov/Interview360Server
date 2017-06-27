from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status

from . import serializers
from . import models

import ipdb

class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.save()
            return Response({'token': serializer.instance.key})
        else:
            return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
