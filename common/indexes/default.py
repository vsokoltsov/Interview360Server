import logging

from elasticsearch_dsl import DocType

from app.credentials.elasticsearch import ELASTICSEARCH_AVAILABLE
from . import INDEX_WARNING_MESSAGE


class DefaultIndex(DocType):
    """ Base class for applications' indexes. """

    @classmethod
    def store_index(cls, user):
        """ Perform check whether or the Elasticsearch is available. """

        if not ELASTICSEARCH_AVAILABLE:
            logging.warning(INDEX_WARNING_MESSAGE)
            return
