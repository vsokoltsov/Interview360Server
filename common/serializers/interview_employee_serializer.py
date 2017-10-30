from rest_framework import serializers
from authorization.serializers import UserSerializer
from companies.models import CompanyMember
from companies.serializers import CompanyMemberSerializer

class InterviewEmployeeSerializer(UserSerializer):
    """ Serializer for interview's employee """

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
