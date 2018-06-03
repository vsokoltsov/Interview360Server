from . import serializers, Interview
from .base_employee_serializer import BaseEmployeeSerializer


class BaseInterviewSerializer(serializers.ModelSerializer):
    """Base Interview serializer class."""

    candidate = serializers.SerializerMethodField()

    class Meta:
        """Base interview serializer metaclass."""

        model = Interview
        fields = [
            'id',
            'candidate',
            'passed',
            'assigned_at',
            'created_at'
        ]

    def get_candidate(self, interview):
        """Receive candidate information."""

        serializer = BaseEmployeeSerializer(
            interview.candidate, read_only=True,
            context={'company_id': interview.vacancy.company.id}
        )
        return serializer.data
