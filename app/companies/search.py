from common.services import SearchService

class CompanySearch(SearchService):
    """ Class for company search methods """

    INDEX_NAME='companies'
    FIELDS=['name', 'description', 'city']
