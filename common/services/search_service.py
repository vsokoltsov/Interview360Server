import logging
from app.settings import ES_CLIENT
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Search


class SearchService:
    """Base service for searching."""

    INDEX_NAME = None
    FIELDS = None

    def __init__(self):
        """Initialize instance.

        Raise exception if index name or index fields are empty.
        """

        if self.INDEX_NAME is None:
            raise Exception(
                'Name of the index cannot be empty.'
                'Redefine index name in child class'
            )
        if self.FIELDS is None:
            raise Exception(
                'Fields cannot be empty. Redefine fields in child class'
            )

    def find(self, query_string, *companies):
        """ Search by given string. """

        if ES_CLIENT is None:
            logging.warning(
                'Elasticsearch is disabled. In order to provide access, \
                    set the ELASTICSEARCH_URL variable'
            )
            return []

        search = Search(using=ES_CLIENT, index=self.INDEX_NAME)
        if query_string:
            query = MultiMatch(
                query=query_string, fuzziness="6", operator="and",
                fields=self.FIELDS
            )
            search = search.query(query)
        else:
            search = search.query()
        if len(companies) > 0:
            search = search.filter('terms', company_id=companies)
        response = search.execute()
        return [hit.to_dict() for hit in response.hits]
