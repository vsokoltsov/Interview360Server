from . import serializers, CompanyMember

class CompanyMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyMember
        fields = [
            'id',
            'role',
            'created_at'
        ]
