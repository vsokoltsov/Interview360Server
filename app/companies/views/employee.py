from . import (
    viewsets, status, Response, Company, get_object_or_404, EmployeeSerializer
)

class EmployeesViewSet(viewsets.ViewSet):
    """ View class for employee's actions """

    def list(self, request, company_pk=None):
        """ Return list of employees for the company """

        company = get_object_or_404(Company, pk=company_pk)
        serializer = EmployeeSerializer(
            company.employees.all(), many=True, context={'company_id': company.id})
        return Response({'employees': serializer.data}, status=status.HTTP_200_OK);
