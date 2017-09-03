from rest_framework import serializers
from .models import Interview, InterviewEmployee
from authorization.models import User
from vacancies.models import Vacancy
from authorization.serializers import UserSerializer
from datetime import datetime
from django.db import transaction
from authorization.serializers import UserSerializer
from vacancies.serializers import VacancySerializer
from companies.models import CompanyMember
from companies.serializers import CompanyMemberSerializer
from roles.constants import CANDIDATE
import ipdb

class InterviewEmployeeSerializer(UserSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ('role', )

    def get_role(self, employee):
        """ Get role for the employee """

        company_id = self.context.get('company_id')
        company_member = CompanyMember.objects.get(user_id=employee.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(company_member, read_only=True).data


class InterviewSerializer(serializers.ModelSerializer):
    """ Class for serialization of Interviews """

    # TODO Validations
    #   - candidate have appropriate role (candidate)

    passed = serializers.BooleanField(read_only=True)
    assigned_at = serializers.DateTimeField(required=True)

    candidate_id = serializers.IntegerField(required=True)
    candidate = serializers.SerializerMethodField(read_only=True)

    vacancy_id = serializers.IntegerField(required=True)
    vacancy = serializers.SerializerMethodField(read_only=True)
    interviewees = serializers.SerializerMethodField(read_only=True)
    interviewees = serializers.ListField(
        required=True, max_length=10,
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Interview
        fields = [
            'id',
            'candidate_id',
            'candidate',
            'vacancy_id',
            'vacancy',
            'passed',
            'assigned_at',
            'created_at',
            'interviewees'
        ]

    def validate_vacancy_id(self, value):
        """ Validation for vacancy_id value """

        try:
            vacancy = Vacancy.objects.get(id=value)
            if not vacancy.active:
                raise serializers.ValidationError("There is no such vacancy")
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("Vacancy is not active")

        return value

    def validate_candidate_id(self, value):
        """ Validation for candidate_id """

        try:
            candidate = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no such candidate")
        return value

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

        serializer = VacancySerializer(interview.vacancy, read_only=True)
        return serializer.data

    def create(self, data):
        """ Create a new instance of interview and some of
            the InterviewEmployee objects """

        interviewees = data.pop('interviewees', None)
        interview = Interview.objects.create(**data)
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
