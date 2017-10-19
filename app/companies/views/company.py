from . import (
    render, viewsets, status, Response, get_object_or_404,
    IsAuthenticated,  TokenAuthentication, Count,
    CompanySerializer, CompaniesSerializer, Company, CompanyPermissions
)

def get_company(user, pk):
    """ Helper method; Receives particular company from the queryset """

    queryset = user.companies.all()
    company = get_object_or_404(queryset, pk=pk)
    return company

class CompaniesViewSet(viewsets.ModelViewSet):
    """ Viewset for company actions """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CompanyPermissions, )

    def get_serializer_class(self):
        """ Return specific serializer for action """

        if self.action == 'list':
            return CompaniesSerializer
        else:
            return CompanySerializer

    def get_queryset(self):
        """
        Return scope of companies which current user belongs to
        """
        
        return self.request.user.companies.prefetched_list()

    def create(self, request):
        """ Creates a new company """

        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response({'company': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Update an existent company """

        company = self.get_object()
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid() and serializer.save():
            return Response({'company': serializer.data},
                        status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ Deletes selected company """

        company = self.get_object()
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
