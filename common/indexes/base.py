import logging

from elasticsearch_dsl import DocType

from companies.index import CompanyIndex, SpecialtyIndex
from resumes.index import ResumesIndex
from skills.index import SkillIndex
from profiles.index import UserIndex
from vacancies.index import VacancyIndex

from app.credentials.elasticsearch import ELASTICSEARCH_AVAILABLE
from . import INDEX_WARNING_MESSAGE


def init_indexes():
    """Init  existing indexes."""

    if not ELASTICSEARCH_AVAILABLE:
        logging.warning(INDEX_WARNING_MESSAGE)
        return

    for item in [
        CompanyIndex, ResumesIndex, SkillIndex, UserIndex, VacancyIndex,
        SpecialtyIndex
    ]:
        try:
            item.init()
        except BaseException:
            pass
