from elasticsearch_dsl import (
    DocType, Date, Float, Integer, Boolean, Keyword, Text, Object
)

class VacancyIndex(DocType):
    """ Vacancy's index class """

    id = Integer()
    title = Text(analyzer='standard')
    description = Text(analyzer='standard')
    salary = Float()
    company_id = Integer()
    active = Boolean()

    class Meta:
        index = 'vacancies'

    @classmethod
    def store_index(cls, vacancy):
        """ Create or update vacancy's index """

        obj = cls(
            meta={'id': vacancy.id},
            id=vacancy.id,
            title=vacancy.title,
            description=vacancy.description,
            salary=vacancy.salary,
            company_id=vacancy.company_id,
            active=vacancy.active
        )
        obj.save()
        return obj.to_dict(include_meta=True)
