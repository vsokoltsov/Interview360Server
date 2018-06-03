from common.services import SearchService


class SkillSearch(SearchService):
    """Class for skill search methods."""

    INDEX_NAME = 'skills'
    FIELDS = ['name']
