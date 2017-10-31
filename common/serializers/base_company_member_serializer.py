from rest_framework import serializers
from companies.models import CompanyMember

class BaseCompanyMemberSerializer(serializers.ModelSerializer):
    """ Base serializer for company member object """

    class Meta:
        model = CompanyMember
        fields = [
            'id',
            'role',
            'created_at'
        ]
