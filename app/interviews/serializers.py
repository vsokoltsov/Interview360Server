from rest_framework import serializers
from .models import Interview, InterviewEmployee
from authorization.models import User
from vacancies.models import Vacancy

class InterviewSerializer(serializers.ModelSerializer):
    """ Class for serialization of Interviews """

    class Meta:
        model = Interview
        fields = [
            'id',
            'candidate',
            'vacancy',
            'passed',
            'assigned_at',
            'created_at',
            'interviewees'
        ]

    # TODO Validations
    #   - vacancy is active
    #   - vacancy is present
    #   - candidate have appropriate role (candidate)
    #   - assigned_at is not lower that today
    #   
