from elasticsearch_dsl import (
    DocType, Date, Float, Integer, Boolean, Keyword, Text, Object
)


class CompanyIndex(DocType):
    """ Company's index class """

    id = Integer()
    name = Text(analyzer='standard')
    description = Text(analyzer='standard')
    city = Text(analyzer='standard')
    start_date = Date()
    attachment = Object()
    vacancy_count = Integer()
    employees_count = Integer()

    class Meta:
        index = 'companies'

    @classmethod
    def store_index(cls, company):
        """ Create or update company's index """

        attachment = company.images.last()
        obj = cls(
            meta={'id': company.id},
            id=company.id,
            name=company.name,
            start_date=company.start_date,
            description=company.description,
            city=company.city,
            attachment=attachment.full_urls() if attachment else None,
            vacancy_count=company.vacancy_set.count(),
            employees_count=company.employees.count()
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class SpecialtyIndex(DocType):
    """ Specialty's index class """

    class Meta:
        index = 'specialties'

    id = Integer()
    name = Text(analyzer='standard')

    @classmethod
    def store_index(cls, specialty):
        """ Create or update specialty's index """

        obj = cls(
            meta={'id': specialty.id},
            id=specialty.id,
            name=specialty.name
        )
        obj.save()
        return obj.to_dict(include_meta=True)
