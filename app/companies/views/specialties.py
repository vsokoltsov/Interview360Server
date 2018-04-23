from . import (
    viewsets, status, Response, IsAuthenticated,  TokenAuthentication, Specialty,
    SpecialtySearch, SpecialtiesSerializer
)
from rest_framework.views import APIView

class SpecialtiesSearchView(APIView):
    """ View class for specialties search """

    def get(self, request, company_pk=None):
        """ Search specialties by given name """

        query = request.query_params.get('q')
        search = SpecialtySearch()
        results = search.find(query)
        return  Response({ 'specialties': results })
