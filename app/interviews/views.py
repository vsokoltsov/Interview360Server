from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InterviewSerializer
# Create your views here.
#
class InterviewViewSet(viewsets.ModelViewSet):
    """ View class for Interviews """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = InterviewSerializer

    def get_queryset(self):
        """
        Return scope of interviews where current user is participated
        """
        user = self.request.user
        return user.interviews.all()
