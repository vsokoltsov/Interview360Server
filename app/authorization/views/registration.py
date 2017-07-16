from . import viewsets, Response, RegistrationForm, status

class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request):
        form = RegistrationForm(request.data)
        
        if form.submit():
            return Response({'token': form.token.key},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST )
