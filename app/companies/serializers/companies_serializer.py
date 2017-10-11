from . import serializers
from .company_serializer import CompanySerializer, BASE_FIELDS

class CompaniesSerializer(CompanySerializer):
    """ Serializer for companies list """

    class Meta:
        model = CompanySerializer.Meta.model
        fields = BASE_FIELDS

    def get_employees_count(self, obj):
        """ Receive number of employees for company """
        
        return obj.employees__count

    def get_vacancy_count(self, obj):
        """ Receive number of vacancies for company """

        return obj.vacancy__count
