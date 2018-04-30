from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.shortcuts import render
from rest_framework import viewsets, status

from .models import Feedback
from .serializers import FeedbackSerializer
from .query import FeedbacksQuery
from .forms import FeedbackForm


class FeedbackViewSet(viewsets.ModelViewSet):
    """ View operations for Feedback """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedbackSerializer
    query_service = FeedbacksQuery

    def get_queryset(self):
        """ Explicitly return the queryset """

        return self.request.user.feedback_set

    def create(self, request):
        """ Create feedback action implementation """

        form = FeedbackForm(params=request.data)
        if form.submit():
            serializer = FeedbackSerializer(form.obj)
            return Response({'feedback': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Update feedback action implementation """

        feedback = self.get_object()
        form = FeedbackForm(obj=feedback, params=request.data)
        if form.submit():
            serializer = FeedbackSerializer(form.obj)
            return Response({'feedback': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)
