from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import list_route
from authorization.models import User

from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ViewSet):
    """ ViewSet for profile operations """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, pk=None):
        """ Return a current user profile information """

        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk=None):
        """ Update current user information """

        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid() and serializer.save():
            return Response(
                { 'current_user': serializer.data }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                { 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST
            )
