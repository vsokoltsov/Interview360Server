from . import (
    viewsets, status, Response
)

class EmployeesViewSet(viewsets.ViewSet):
    """ View class for employee's actions """

    def list(self, request, company_pk=None):
        """ Return list of employees for the company """
        return Response({'employees': []}, status=status.HTTP_200_OK);
