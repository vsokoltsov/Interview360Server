from . import (
    serializers, ResumesSerializer, Resume, User, SkillSerializer, UserSerializer,
    CustomField, ResumesIndex, WorkplaceSerializer
)

class ResumeSerializer(ResumesSerializer):
    """ Resume serializer class """

    skills = SkillSerializer(many=True)
    workplaces = WorkplaceSerializer(many=True)

    class Meta(ResumesSerializer.Meta):
        model = ResumesSerializer.Meta.model
        fields = ResumesSerializer.Meta.fields + [
            'description',
            'skills',
            'workplaces',
            'created_at'
        ]
