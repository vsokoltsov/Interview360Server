from elasticsearch_dsl import (
    DocType, Date, Float, Integer, Boolean, Keyword, Text, Object
)

class CompanyIndex(DocType):
    """ Company's index class """

    id = Integer()
    name = Text(analyzer='standard')
    description = Text(analyzer='standard')
    city = Text(analyzer='standard')

    class Meta:
        index = 'companies'

    @classmethod
    def store_index(cls, company):
        """ Create or update company's index """

        obj = cls(
            meta={'id': company.id},
            id=company.id,
            name=company.name,
            description=company.description,
            city=company.city
        )
        obj.save()
        return obj.to_dict(include_meta=True)
