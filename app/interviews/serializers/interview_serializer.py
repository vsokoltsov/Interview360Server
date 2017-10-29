from . import serializers, Interview, InterviewEmployee

from authorization.models import User
from companies.models import Company, CompanyMember
from vacancies.models import Vacancy
from datetime import datetime
from django.db import transaction
from authorization.serializers import UserSerializer
from common.serializers.base_vacancy_serializer import BaseVacancySerializer
from .interview_employee_serializer import InterviewEmployeeSerializer
from roles.constants import CANDIDATE
import ipdb

class InterviewSerializer(serializers.ModelSerializer):
    """ Class for serialization of Interviews """

    # TODO Validations
    #   - candidate have appropriate role (candidate)

    passed = serializers.BooleanField(read_only=True)
    assigned_at = serializers.DateTimeField(required=True)

    candidate_email = serializers.CharField(required=True, max_length=255)
    candidate = serializers.SerializerMethodField(read_only=True)

    vacancy_id = serializers.IntegerField(required=True)
    vacancy = serializers.SerializerMethodField(read_only=True)
    interviewees = serializers.SerializerMethodField(read_only=True)
    interviewee_ids = serializers.ListField(
        required=True, max_length=10,
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Interview
        fields = [
            'id',
            'candidate_email',
            'candidate',
            'vacancy_id',
            'vacancy',
            'passed',
            'assigned_at',
            'created_at',
            'interviewees',
            'interviewee_ids'
        ]

    def validate_vacancy_id(self, value):
        """ Validation for vacancy_id value """

        try:
            vacancy = Vacancy.objects.get(id=value)
            if not vacancy.active:
                raise serializers.ValidationError("Vacancy is not active")
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("There is no such vacancy")

        return value
    #
    # def validate_candidate_id(self, value):
    #     """ Validation for candidate_id """
    #
    #     try:
    #         candidate = User.objects.get(id=value)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("There is no such candidate")
    #     return value

    def validate_assigned_at(self, value):
        """ Validation for assigned_at field """

        if value.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError("Selected datetime is less than current")

        return value

    def get_candidate(self, interview):
        """ Retrieve candidate serializer """

        serializer = InterviewEmployeeSerializer(
            interview.candidate, read_only=True,
            context={'company_id': interview.vacancy.company.id }
        )
        return serializer.data

    def get_interviewees(self, interview):
        """ Retrieve candidate interviewees list """

        serializer = InterviewEmployeeSerializer(
            interview.interviewees.all(), read_only=True, many=True,
            context={'company_id': interview.vacancy.company.id }
        )

        return serializer.data

    def get_vacancy(self, interview):
        """ Rertrieve vacancy serializer """

        serializer = BaseVacancySerializer(interview.vacancy, read_only=True)
        return serializer.data

    def create(self, data):
        """ Create a new instance of interview and some of
            the InterviewEmployee objects """

        interviewees = data.pop('interviewee_ids', None)
        candidate_email = data.pop('candidate_email', None)
        candidate_id = self._get_or_create_candidate(candidate_email, data)
        interview = Interview.objects.create(**data, candidate_id=candidate_id)
        if interviewees:
            for employee_id in interviewees:
                employee = User.objects.get(id=employee_id)
                InterviewEmployee.objects.create(
                    interview_id=interview.id, employee_id=employee.id
                )
        return interview

    def update(self, instance, data):
        """ Update an existed instance of interview """

        instance.assigned_at = data.get('assigned_at', instance.assigned_at)

        return instance

    def _get_or_create_candidate(self, email, data):
        """ Get or create a new user object for a candidate based on the email """

        candidate = User.objects.get_or_create(email=email)
        vacancy_id = data.pop('vacancy_id')
        vacancy = Vacancy.objects.get(pk=vacancy_id)
        try:
            candidate.companies.get(id=vacancy.company_id)
        except Company.DoesNotExist:
            CompanyMember.objects.create(
                user_id=candidate.id,
                company_id=vacancy.company_id,
                role=CANDIDATE
            )
        finally:
            return candidate.id
