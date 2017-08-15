from . import serializers, User, CompanyMember
from .company_member_serializer import CompanyMemberSerializer
from authorization.serializers import UserSerializer

class EmployeeSerializer(UserSerializer):
    """ Company employee serializer class """

    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('roles',)

    def get_roles(self, obj):
        """ Receiving list of Employee objects """

        company_id = self.context.get('company_id')
        queryset = CompanyMember.objects.filter(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(queryset, many=True, read_only=True).data
