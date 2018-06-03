from . import viewsets, status, Response, RestorePasswordForm


class RestorePasswordViewSet(viewsets.ViewSet):
    """Restore password view."""

    def create(self, request):
        """Restore user's password; Send email with instructions."""

        form = RestorePasswordForm(request.data)

        if form.submit():
            return Response({'message': 'Mail was succesfully sended'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)
