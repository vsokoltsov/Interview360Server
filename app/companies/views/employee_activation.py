from . import Response, get_object_or_404, User, Company, EmployeeForm, status
from rest_framework.views import APIView

class EmployeeActivationView(APIView):

    def put(self, request, company_id):
        form = EmployeeForm(request.data)

        if form.submit():
            return Response(
                { 'message': 'You was sucessfully added to the company!' },
                status=status.HTTTP_200_OK
            )
        else:
            return Response(
                { 'errors': form.errors },
                status=status.HTTP_400_BAD_REQUEST
            )
