from rest_framework import serializers
from companies.models import CompanyMember


class BaseCompanyMemberSerializer(serializers.ModelSerializer):
    """Base serializer for company member object."""

    class Meta:
        """Metaclass for serializer."""

        model = CompanyMember
        fields = [
            'id',
            'role',
            'created_at'
        ]
