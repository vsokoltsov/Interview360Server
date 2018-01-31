from authorization.models import User
from profiles.index import UserIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging

def rebuild_index():
    """ Rebuild index for the users """

    try:
        Index('users').delete()
    except TransportError:
        logging.logger.warning('There is no such index')
    finally:
        UserIndex.init()
        users = User.objects.prefetch_related('companies', 'attachments')
        for user in users:
            print(UserIndex.store_index(user))
