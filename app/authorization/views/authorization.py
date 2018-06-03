from . import viewsets, Response, AuthorizationForm, status


class AuthorizationViewSet(viewsets.ViewSet):
    """Authorization view class."""

    def create(self, request):
        """Authorize user."""

        form = AuthorizationForm(request.data)

        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)
