from . import (TokenAuthentication, IsAuthenticated,
               CurrentUserSerializer, Response, APIView)


class CurrentUserView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'current_user': CurrentUserSerializer(request.user).data
        })
