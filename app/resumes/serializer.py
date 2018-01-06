from rest_framework import serializers
from .models import Resume
from authorization.models import User
from vacancies.fields import SkillsField
from common.serializers.user_serializer import UserSerializer
from common.fields import CustomField
import ipdb

class ResumesSerializer(serializers.ModelSerializer):
    """ Resumes serializer class """

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'user',
            'updated_at'
        ]

class ResumeSerializer(ResumesSerializer):
    """ Resume serializer class """

    title = serializers.CharField(required=True)
    user = CustomField(serializer=UserSerializer, obj='user', required=True)
    description = serializers.CharField(required=True)
    skills = SkillsField(required=True)

    class Meta(ResumesSerializer.Meta):
        model = ResumesSerializer.Meta.model
        fields = ResumesSerializer.Meta.fields + [
            'description',
            'skills',
            'created_at'
        ]

    def create(self, data):
        """ Create new resume instance """

        skills = data.pop('skills', None)
        resume = Resume.objects.create(**data)
        resume.skills.set(skills)
        return resume

    def update(self, instance, data):
        """ Update resume instance """

        instance.description = data.get('description', instance.description)
        instance.skills.set(data.get('skills', []))
        instance.save()
        return instance
