from companies.models import Company
from companies.index import CompanyIndex
from elasticsearch_dsl import Index
from elasticsearch.exceptions import TransportError
import logging

def rebuild_company_index():
    """ Rebuild index for the companies """

    try:
        Index('companies').delete()
    except TransportError:
        loggin.logger.warning('There is no such index')
    finally:
        CompanyIndex.init()
        companies = Company.objects.all()
        for company in companies:
            print(CompanyIndex.store_index(company))
