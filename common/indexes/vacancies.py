from vacancies.models import Vacancy
from vacancies.index import VacancyIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging

def rebuild_vacancy_index():
    """ Rebuild index for the vacancies """

    try:
        Index('vacancies').delete()
    except TransportError:
        logging.logger.warning('There is no such index')
    finally:
        VacancyIndex.init()
        vacancies = Vacancy.objects.all()
        for vacancy in vacancies:
            print(VacancyIndex.store_index(vacancy))
