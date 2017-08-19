from . import (
    viewsets, status, Response, Company, get_object_or_404,
    EmployeeSerializer, User, IsAuthenticated,  TokenAuthentication
)
from rest_framework.decorators import list_route

class EmployeesViewSet(viewsets.ViewSet):
    """ View class for employee's actions """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def list(self, request, company_pk=None):
        """ Return list of employees for the company """

        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(
            company.employees.all(), many=True, context={'company_id': company.id})
        return Response({'employees': serializer.data}, status=status.HTTP_200_OK);

    def create(self, request, company_pk=None):
        """ Create new user and send it a letter """
        
        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(request.data, context={'user': request.user})

        if serializer.is_valid() and serializer.save():
            return Response({ 'message': 'Users were succesfully added as an employee' })
        else:
            return Response({ 'errors': serializer.error })

    @list_route(methods=['put'])
    def activate(self, request, company_pk=None):
        """
        Activate employee for the company by creating CompanyMember
        and setting user password
        """
        pass

    def get_company(self, id):
        return get_object_or_404(Company, pk=id)
