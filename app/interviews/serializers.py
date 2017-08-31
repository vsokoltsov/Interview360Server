from rest_framework import serializers
from .models import Interview, InterviewEmployee
from authorization.models import User
from vacancies.models import Vacancy
from authorization.serializers import UserSerializer
import ipdb

class InterviewSerializer(serializers.ModelSerializer):
    """ Class for serialization of Interviews """

    passed = serializers.BooleanField(read_only=True)
    assigned_at = serializers.DateTimeField(required=True)

    candidate_id = serializers.IntegerField(required=True)
    candidate = serializers.SerializerMethodField(read_only=True)

    vacancy_id = serializers.IntegerField(required=True)
    vacancy = serializers.SerializerMethodField(read_only=True)


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

    def validate_candidate_id(self, value):
        """ Validation for candidate_id """

        try:
            candidate = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no such candidate")


    # TODO Validations
    #   - vacancy is active
    #   - vacancy is present
    #   - candidate have appropriate role (candidate)
    #   - assigned_at is not lower that today
    #
