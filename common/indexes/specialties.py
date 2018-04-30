from companies.models import Specialty
from companies.index import SpecialtyIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging


def rebuild_index():
    """ Rebuild skills index """

    try:
        Index('specialties').delete()
    except TransportError:
        logging.logger.warning('There is no such index')
    finally:
        SpecialtyIndex.init()
        skills = Specialty.objects.all()
        for skill in skills:
            print(SpecialtyIndex.store_index(skill))
