from . import serializers
from common.serializers.base_company_serializer import BaseCompanySerializer


class CompaniesSerializer(BaseCompanySerializer):
    """Serializer for companies list."""

    employees_count = serializers.SerializerMethodField()
    vacancy_count = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta class."""

        model = BaseCompanySerializer.Meta.model
        fields = BaseCompanySerializer.Meta.fields + [
            'employees_count', 'vacancy_count'
        ]

    def get_employees_count(self, obj):
        """Receive number of employees for company."""

        return obj.employees__count

    def get_vacancy_count(self, obj):
        """Receive number of vacancies for company."""

        return obj.vacancy__count
