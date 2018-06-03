from . import viewsets, Response, RegistrationForm, status


class RegistrationViewSet(viewsets.ViewSet):
    """User registration view class."""

    def create(self, request):
        """Create new user."""

        form = RegistrationForm(request.data)

        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)
