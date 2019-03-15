from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from skills.serializers import SkillSerializer
import ipdb


class SkillsField(serializers.Field):
    """Custom field for 'skills' attribute in request."""

    def get_attribute(self, obj):
        """Return serialized value."""

        skills = obj.skills.all()
        if skills:
            return SkillSerializer(skills, many=True).data
        else:
            return None

    def to_representation(self, obj):
        """Return external representation."""

        return obj

    def to_internal_value(self, data):
        """Return internal representation."""

        return data
