from . import serializers, CompanyMember
from .company_member_serializer import CompanyMemberSerializer
from common.serializers.user_serializer import UserSerializer

class EmployeeSerializer(UserSerializer):
    """ Company employee serializer class """

    member_role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ('member_role', )
        read_only_fields = UserSerializer.Meta.fields

    def get_member_role(self, obj):
        """ Get role for the employee """

        company_id = self.context.get('company_id')
        company_member = CompanyMember.objects.get(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(company_member, read_only=True).data
