from . import viewsets, Response, AuthorizationForm, status

class AuthorizationViewSet(viewsets.ViewSet):

    def create(self, request):
        form = AuthorizationForm(request.data)
        
        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST )
