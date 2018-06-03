from . import (TokenAuthentication, IsAuthenticated,
               CurrentUserSerializer, Response, APIView)


class CurrentUserView(APIView):
    """Current user view class."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """Return current user information."""

        return Response({
            'current_user': CurrentUserSerializer(request.user).data
        })
