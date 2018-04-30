from skills.models import Skill
from skills.index import SkillIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging


def rebuild_index():
    """ Rebuild skills index """

    try:
        Index('skills').delete()
    except TransportError:
        logging.logger.warning('There is no such index')
    finally:
        SkillIndex.init()
        skills = Skill.objects.all()
        for skill in skills:
            print(SkillIndex.store_index(skill))
