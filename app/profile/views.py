from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import list_route

from .serializers import ProfileSerializer

class ProfileAPIView(APIView):
    """ ViewSet for profile operations """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """ Return a current user profile information """

        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        """ Update current user information """

        serializer = ProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid() and serializer.save():
            return Response(
                { 'current_user': serializer.data }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                { 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST
            )
