from . import serializers, User, CompanyMember
from .company_member_serializer import CompanyMemberSerializer

class CompanyEmployeeSerializer(serializers.ModelSerializer):
    """ Company employee serializer class """

    company_members = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'company_members'
        ]

    def get_company_members(self, obj):
        """ Receiving list of CompanyMember objects """

        company_id = self.context.get('company_id')
        queryset = CompanyMember.objects.filter(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(queryset, many=True, read_only=True).data
