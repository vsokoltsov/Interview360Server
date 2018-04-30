from elasticsearch_dsl import (
    DocType, Integer, Text
)


class SkillIndex(DocType):
    """ Skill's index class """

    id = Integer()
    name = Text(analyzer='standard')

    class Meta:
        index = 'skills'

    @classmethod
    def store_index(cls, skill):
        """ Create or update skill's index """

        obj = cls(
            meta={'id': skill.id},
            id=skill.id,
            name=skill.name
        )
        obj.save()
        return obj.to_dict(include_meta=True)
