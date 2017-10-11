from . import serializers
from .company_serializer import CompanySerializer, BASE_FIELDS

class CompaniesSerializer(CompanySerializer):
    """ Serializer for companies list """

    employees_count = serializers.SerializerMethodField()
    vacancy_count = serializers.SerializerMethodField()

    class Meta:
        model = CompanySerializer.Meta.model
        fields = BASE_FIELDS + [
            'employees_count',
            'vacancy_count'
        ]

    def get_employees_count(self, obj):
        """ Receive number of employees for company """

        return obj.employees__count

    def get_vacancy_count(self, obj):
        """ Receive number of vacancies for company """

        return obj.vacancy__count
