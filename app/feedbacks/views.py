from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Feedback
from .serializers import FeedbackSerializer
from .query import FeedbacksQuery

class FeedbackViewSet(viewsets.ViewSet):
    """ View operations for Feedback """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedbackSerializer
    query_service = FeedbacksQuery

    @list_route(methods=['get'])
    def mine(self, request):
        """ Routes for feedbacks on me """

        queryset = self.query_service(self.request.user).mine()
        return Response({ 'feedbacks': queryset }, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def others(self, request):
        """ Route for my feedbacks on other users  """

        queryset = self.query_service(self.request.user).others()
        return Response({ 'feedbacks': queryset }, status=status.HTTP_200_OK)
