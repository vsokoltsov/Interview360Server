from elasticsearch_dsl import (
    DocType, Date, Float, Integer, Boolean, Keyword, Text, Object
)
from skills.models import Skill
from common.indexes.default import DefaultIndex


class ResumesIndex(DefaultIndex):
    """Resumes index class."""

    id = Integer()
    title = Text(analyzer='standard')
    description = Text(analyzer='standard')
    skills = Keyword()
    user = Text(analyzer='standard')
    created_at = Date()
    updated_at = Date()

    class Meta:
        """Metaclass for index."""

        index = 'resumes'

    @classmethod
    def store_index(cls, resume):
        """Create or update resume's index."""

        if resume.user.first_name and resume.user.last_name:
            user = '{} {}'.format(
                resume.user.first_name,
                resume.user.last_name)
        else:
            user = resume.user.email
        skills = list(map(lambda s: s.name, Skill.objects.all()))
        obj = cls(
            meta={'id': resume.id},
            id=resume.id,
            title=resume.title,
            description=resume.description,
            skills=skills,
            user=user,
            created_at=resume.created_at,
            updated_at=resume.updated_at
        )
        obj.save()
        return obj.to_dict(include_meta=True)
