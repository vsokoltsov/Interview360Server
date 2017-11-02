from authorization.models import User
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text

class UserIndex(DocType):
    """ User class index """

    id = Integer()
    first_name = Text(analyzer='snowball')
    last_name = Text(analyzer='snowball')
    email = Text(analyzer='snowball')
    company_ids = Integer()

    class Meta:
        index = 'users'

def rebuild_index():
    """ Rebuild index for the users """

    UserIndex.init()
    users = User.objects.prefetch_related('companies', 'attachments')
    for user in users:
        company_ids = list(
            map(lambda c: c.id, user.companies.all())
        )
        obj = UserIndex(
            meta={'id': user.id},
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_ids=company_ids
        )
        obj.save()
        print(obj.to_dict(include_meta=True))
