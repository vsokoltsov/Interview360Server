from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route
from .permissions import UserProfilePermission
from .forms import ChangePasswordForm
from authorization.models import User

from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ViewSet):
    """ ViewSet for profile operations """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, UserProfilePermission, )

    def retrieve(self, request, pk=None):
        """ Return a current user profile information """

        user = self.get_object(pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """ Update current user information """

        user = self.get_object(pk)
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

    @detail_route(methods=['put'], permission_classes=(IsAuthenticated, UserProfilePermission, ))
    def change_password(self, request, pk=None):
        """ Handle change password update """

        user = self.get_object(pk)
        form = ChangePasswordForm(user, request.data)
        if form.submit():
            return Response(
                {'message': 'Password was succesfully updated'}
            )
        else:
            return Response(
                { 'errors': form.errors }, status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self, pk):
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
