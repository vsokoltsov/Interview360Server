from resumes.models import Resume
from resumes.index import ResumesIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging


def rebuild_index():
    """Rebuild resumes index."""

    try:
        Index('resumes').delete()
    except TransportError:
        logging.logger.warning('There is no such index')
    finally:
        ResumesIndex.init()
        resumes = Resume.objects.all()
        for resume in resumes:
            print(ResumesIndex.store_index(resume))
