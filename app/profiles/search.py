from app.settings import ES_CLIENT
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Search
from common.services import SearchService

class UsersSearch(SearchService):
    """ Class for user search methods """

    INDEX_NAME='users'
    FIELDS=['email', 'first_name', 'last_name']
