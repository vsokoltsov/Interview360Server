from vacancies.models import Vacancy
from vacancies.index import VacancyIndex
from elasticsearch_dsl import Index

def rebuild_vacancy_index():
    """ Rebuild index for the vacancies """

    Index('vacancies').delete()
    VacancyIndex.init()
    vacancies = Vacancy.objects.all()
    for vacancy in vacancies:
        print(VacancyIndex.store_index(vacancy))
