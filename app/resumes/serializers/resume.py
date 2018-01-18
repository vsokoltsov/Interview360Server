from . import (
    serializers, ResumesSerializer, Resume, User, SkillsField, UserSerializer,
    CustomField, ResumesIndex
)

class ResumeSerializer(ResumesSerializer):
    """ Resume serializer class """

    title = serializers.CharField(required=True)
    user = CustomField(serializer=UserSerializer, obj='user', required=True)
    description = serializers.CharField(required=True)
    salary = serializers.DecimalField(max_digits=8, decimal_places=0, required=True)
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
        ResumesIndex.store_index(resume)
        return resume

    def update(self, instance, data):
        """ Update resume instance """

        instance.description = data.get('description', instance.description)
        instance.skills.set(data.get('skills', []))
        instance.save()
        ResumesIndex.store_index(instance)
        return instance
