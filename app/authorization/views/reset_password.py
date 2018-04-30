from . import viewsets, Response, status, ResetPasswordForm


class ResetPasswordViewSet(viewsets.ViewSet):

    def create(self, request):
        form = ResetPasswordForm(request.data)

        if form.submit():
            return Response({'message': 'Your password was succesfully restored'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)
