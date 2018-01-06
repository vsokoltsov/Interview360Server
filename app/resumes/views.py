from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .serializers import ResumesSerializer, ResumeSerializer

class ResumeView(viewsets.ModelViewSet):
    """ Resume views """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        """ Return specific serializer for action """

        if self.action == 'list':
            return ResumesSerializer
        else:
            return ResumeSerializer

    def create(self, request):
        """ Create a new resume """

        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'resume': serializer.data},
                        status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Update existing resume """

        resume = self.get_object()
        serializer = ResumeSerializer(resume, data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'resume': serializer.data},
                        status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ Deletes selected resume """

        resume = self.get_object()
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
