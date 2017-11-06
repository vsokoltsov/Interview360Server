from vacancies.models import Vacancy
from vacancies.index import VacancyIndex
from elasticsearch_dsl import Index

def rebuild_vacancy_index():
    """ Rebuild index for the vacancies """

    VacancyIndex.init()
    Index('vacancies')
    vacancies = Vacancy.objects.all()
    for vacancy in vacancies:
        print(VacancyIndex.store_index(vacancy))
