from . import viewsets, list_route, Response, status
from resumes.forms import WorkplaceForm
from resumes.serializers import WorkplaceSerializer

class WorkplacesViewSet(viewsets.ModelViewSet):
    """ Views for workplace resource """

    @list_route(methods='PUT')
    def update(self, request, resume_id=None):
        """ Create new workplaces for resume; Update existing ones """

        form = WorkplaceForm(params=request.data)
        if form.submit():
            return Response(
                { 'workplaces': WorkplaceSerializer(form.objects, many=True).data }
            )
        else:
            return Response(
                { 'errors': form.errors }, status=status.HTTP_400_BAD_REQUEST
            )
