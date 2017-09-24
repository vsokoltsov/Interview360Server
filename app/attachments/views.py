from django.shortcuts import render
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import AttachmentSerializer
import ipdb

class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
