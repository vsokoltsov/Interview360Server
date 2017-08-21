from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    """ Serializer for Role objects """

    class Meta:
        model = Role
        fields = ('id', 'name', 'created_at')
