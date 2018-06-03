from common.services import SearchService


class CompanySearch(SearchService):
    """Class for company search methods."""

    INDEX_NAME = 'companies'
    FIELDS = ['name', 'description', 'city']


class SpecialtySearch(SearchService):
    """Class for specialty search methods."""

    INDEX_NAME = 'specialties'
    FIELDS = ['name']
