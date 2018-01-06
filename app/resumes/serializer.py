from rest_framework import serializers
from .models import Resume
from authorization.models import User
from vacancies.fields import SkillsField
from common.serializers.user_serializer import UserSerializer
from common.fields import CustomField
import ipdb

class ResumeSerializer(serializers.ModelSerializer):
    """ Resume serializer class """

    user = CustomField(serializer=UserSerializer, obj='user')
    description = serializers.CharField(required=True)
    skills = SkillsField(required=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'description',
            'skills',
            'user'
        ]

    def create(self, data):
        """ Create new resume instance """

        skills = data.pop('skills', None)
        resume = Resume.objects.create(**data)
        resume.skills.set(skills)
        return resume
