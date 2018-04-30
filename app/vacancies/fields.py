from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from skills.serializers import SkillSerializer
import ipdb


class SkillsField(serializers.Field):
    """ Custom field for 'skills' attribute in request """

    def get_attribute(self, obj):
        skills = obj.skills.all()
        if skills:
            return SkillSerializer(skills, many=True).data
        else:
            return None

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data
