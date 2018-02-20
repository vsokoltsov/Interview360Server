from . import serializers, Resume
from skills.models import Skill
from skills.serializers import SkillSerializer
from resumes.query import ResumesQuery

class ResumesFilter(serializers.Serializer):
    """ Serializer for the resumes filter """

    skills = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()

    def get_skills(self, object):
        """ Receive the list of the most frequent skills for all resumes """

        skills_list = Resume.objects.values_list('skills', flat=True)
        skills = Skill.objects.filter(id__in=[item for item in skills_list])
        return SkillSerializer(skills, many=True).data

    def get_order(self, object):
        """ Get list of available items for ordering """

        return ResumesQuery.VALID_ORDER_FIELDS

    def get_salary(self, object):
        """ Get object for the minimum and maximum salary """

        return Resume.objects.aggregate(min=Min('salary'), max=Max('salary'))
