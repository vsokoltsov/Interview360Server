from django.shortcuts import render
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ImageSerializer
import ipdb


class AttachmentViewSet(viewsets.ViewSet):
    """ Attachment view class """

    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid() and serializer.save():
            return Response(
                {'attachment': serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
