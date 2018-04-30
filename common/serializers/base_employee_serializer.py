from rest_framework import serializers
from .user_serializer import UserSerializer
from .base_company_member_serializer import BaseCompanyMemberSerializer
from companies.models import CompanyMember


class BaseEmployeeSerializer(UserSerializer):
    """ Base serializer for employee """

    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ('role', )

    def get_role(self, employee):
        """ Get role for the employee """

        company_id = self.context.get('company_id')
        company_member = CompanyMember.objects.get(user_id=employee.id,
                                                   company_id=company_id)
        return BaseCompanyMemberSerializer(company_member, read_only=True).data
