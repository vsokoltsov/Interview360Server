from app.settings import ES_CLIENT
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Search

class UsersSearch:
    """ Class for user search methods """

    INDEX_NAME='users'

    def find_users(self, query_string):
        """ Find users inside given values """

        search = Search(using=ES_CLIENT, index=self.INDEX_NAME)
        query =  MultiMatch(
            query=query_string, fuzziness="6", operator="and",
            fields=['email', 'first_name', 'last_name']
        )
        search = search.query(query)
        response = search.execute()
        return [hit.to_dict() for hit in response.hits]
