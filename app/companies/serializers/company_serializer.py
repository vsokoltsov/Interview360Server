from . import (
    serializers
)
from .companies_serializer import CompaniesSerializer
from .employee_serializer import EmployeeSerializer
from .specialties_serializer import SpecialtiesSerializer
from common.serializers.base_vacancy_serializer import BaseVacancySerializer
from common.serializers.base_interview_serializer import (
    BaseInterviewSerializer
)
from interviews.models import Interview


class CompanySerializer(CompaniesSerializer):
    """Serialization of Company object."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    city = serializers.CharField(required=True, max_length=255)
    country = serializers.CharField(required=True, max_length=255)
    employees = serializers.SerializerMethodField()
    vacancies = serializers.SerializerMethodField()
    interviews = serializers.SerializerMethodField()
    specialties = SpecialtiesSerializer(many=True)

    class Meta:
        """Company's serializer meta class."""

        model = CompaniesSerializer.Meta.model
        fields = CompaniesSerializer.Meta.fields + [
            'employees', 'vacancies', 'interviews', 'specialties'
        ]

    def get_employees(self, obj):
        """Receives the list of employees."""

        employees_list = obj.employees.prefetch_related('avatars')[:5]
        return EmployeeSerializer(
            employees_list, many=True, read_only=True,
            context={'company_id': obj.id}
        ).data

    def get_vacancies(self, obj):
        """Receive a list of vacancies for company."""

        vacancies_list = obj.vacancy_set.all()[:5]
        return BaseVacancySerializer(
            vacancies_list, many=True, read_only=True
        ).data

    def get_interviews(self, obj):
        """Receive a list of interviews for company."""

        interviews = Interview.for_company(obj.id)
        return BaseInterviewSerializer(
            interviews, many=True, read_only=True
        ).data

    def get_employees_count(self, obj):
        """Receive number of employees for company."""

        try:
            return obj.employees__count
        except AttributeError:
            return obj.employees.count()

    def get_vacancy_count(self, obj):
        """Receive number of vacancies for company."""

        try:
            return obj.vacancy__count
        except AttributeError:
            return obj.vacancy_set.count()
