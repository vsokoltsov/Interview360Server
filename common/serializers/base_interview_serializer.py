from . import serializers, Interview
# import ipdb; ipdb.set_trace()
# from .interview_employee_serializer import InterviewEmployeeSerializer

class BaseInterviewSerializer(serializers.ModelSerializer):

    candidate = serializers.SerializerMethodField()

    class Meta:
        model = Interview
        fields = [
            'id',
            'candidate',
            'passed',
            'assigned_at',
            'created_at'
        ]

    def get_candidate(self, interview):
        """ Receive candidate information """

        import ipdb; ipdb.set_trace()
        serializer = InterviewEmployeeSerializer(
            interview.candidate, read_only=True,
            context={'company_id': interview.vacancy.company.id }
        )
        return serializer.data
