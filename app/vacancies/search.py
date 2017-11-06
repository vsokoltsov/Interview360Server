from common.services import SearchService

class VacancySearch(SearchService):
    """ Class for user search methods """

    INDEX_NAME='vacancies'
    FIELDS=['title', 'description']
