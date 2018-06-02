from . import (
    viewsets, list_route, Response, status, IsAuthenticated,
    TokenAuthentication, WorkplacePermissions
)
from rest_framework.views import APIView
from resumes.forms import WorkplaceForm
from resumes.serializers import WorkplaceSerializer


class WorkplacesApiView(APIView):
    """Views for workplace resource."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, WorkplacePermissions, )

    def put(self, request, resume_id=None):
        """
        Create new workplaces for resume.

        Update existing ones.
        """

        form = WorkplaceForm(params=request.data)
        if form.submit():
            serialized_data = WorkplaceSerializer(form.objects, many=True).data
            return Response(
                {'workplaces': serialized_data}
            )
        else:
            return Response(
                {'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST
            )
