from common.services import SearchService

class ResumesSearch(SearchService):
    """ Class for resumes search methods """

    INDEX_NAME='resumes'
    FIELDS=['title', 'description', 'user', 'skills']
