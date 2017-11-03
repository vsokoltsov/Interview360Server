from . import (
    viewsets, status, Response, Company, CompanyMember, get_object_or_404,
    EmployeeSerializer, User, IsAuthenticated,  TokenAuthentication, User,
    EmployeePermission, list_route, UsersSearch, UserIndex
)

class EmployeesViewSet(viewsets.ViewSet):
    """ View class for employee's actions """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, EmployeePermission, )

    def list(self, request, company_pk=None):
        """ Return list of employees for the company """

        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(
            company.employees.all(), many=True, context={'company_id': company.id})
        return Response({'employees': serializer.data}, status=status.HTTP_200_OK);

    def create(self, request, company_pk=None):
        """ Create new user and send it a letter """

        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid() and serializer.save():
            return Response(
                { 'message': 'Users were succesfully added as an employee' },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                { 'errors': serializer.errors },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, company_pk=None, pk=None):
        """ Destroys the CompanyMember object  """

        company = self.get_company(company_pk)
        employee = get_object_or_404(User, pk=pk)
        company_member = CompanyMember.objects.get(
            user_id=employee.id, company_id=company.id
        )
        company_member.delete()
        UserIndex.get(id=employee.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_company(self, id):
        return get_object_or_404(Company, pk=id)

    @list_route(methods=['get'])
    def search(self, request, company_pk=None):
        """ Action for user search """

        query = request.query_params.get('q')
        search = UsersSearch()
        results = search.find_users(query, company_pk)
        return  Response({ 'users': results })
