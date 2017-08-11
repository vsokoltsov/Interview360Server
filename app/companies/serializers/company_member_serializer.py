from . import serializers, CompanyMember

class CompanyMemberSerializer(serializers.ModelSerializer):
    """ CompanyMember serializer class """
    
    class Meta:
        model = CompanyMember
        fields = [
            'id',
            'role',
            'created_at'
        ]
