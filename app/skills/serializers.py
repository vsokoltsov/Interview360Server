from rest_framework import serializers
from .models import Skill

class SkillSerializer(serializers.ModelSerializer):
    """ Serializer for Skill objects """

    class Meta:
        model = Skill
        fields = ('id', 'name', 'created_at')
