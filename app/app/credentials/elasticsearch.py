"""
Elasticsearch base configruation.
"""

import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

ELASTICSEARCH_AVAILABLE = False

es_host = os.environ.get('ELASTICSEARCH_URL')
if es_host:
    ES_CLIENT = Elasticsearch(['{}'.format(es_host)])
    connections.create_connection(hosts=['{}'.format(es_host)])
    ELASTICSEARCH_AVAILABLE = True
