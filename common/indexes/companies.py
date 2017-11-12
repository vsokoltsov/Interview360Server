from companies.models import Company
from companies.index import CompanyIndex
from elasticsearch_dsl import Index

def rebuild_company_index():
    """ Rebuild index for the companies """

    Index('companies').delete()
    CompanyIndex.init()
    companies = Company.objects.all()
    for company in companies:
        print(CompanyIndex.store_index(company))
