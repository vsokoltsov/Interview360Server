from . import (
    serializers, ResumesSerializer, Resume, User, SkillSerializer, UserSerializer,
    CustomField, ResumesIndex, WorkplaceSerializer, ContactSerializer
)

class ResumeSerializer(ResumesSerializer):
    """ Resume serializer class """

    skills = SkillSerializer(many=True)
    contact = ContactSerializer()
    workplaces = WorkplaceSerializer(many=True)

    class Meta(ResumesSerializer.Meta):
        model = ResumesSerializer.Meta.model
        fields = ResumesSerializer.Meta.fields + [
            'description',
            'skills',
            'workplaces',
            'contact',
            'created_at'
        ]
