from . import serializers, Resume

from django.db.models import Max, Min
from skills.models import Skill
from skills.serializers import SkillSerializer
from resumes.query import ResumesQuery


class ResumesFilter(serializers.Serializer):
    """Serializer for the resumes filter."""

    skills = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()

    class Meta:
        """Metaclass for serializer."""

        fields = [
            'skills',
            'order',
            'salary'
        ]

    def get_skills(self, obj):
        """Receive the list of the most frequent skills for all resumes."""

        skills_list = Resume.objects.values_list('skills', flat=True)
        skills = Skill.objects.filter(id__in=[item for item in skills_list])
        return SkillSerializer(skills, many=True).data

    def get_order(self, obj):
        """Get list of available items for ordering."""

        return ResumesQuery.order_fields

    def get_salary(self, obj):
        """Get object for the minimum and maximum salary."""

        return Resume.objects.aggregate(min=Min('salary'), max=Max('salary'))
