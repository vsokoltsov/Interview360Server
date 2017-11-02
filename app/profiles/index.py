# from authorization.models import User
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Object

class UserIndex(DocType):
    """ User class index """

    id = Integer()
    first_name = Text(analyzer='snowball')
    last_name = Text(analyzer='snowball')
    email = Text(analyzer='snowball')
    company_ids = Integer()
    attachment = Object()

    class Meta:
        index = 'users'

    @classmethod
    def store_index(cls, user):
        """ Create or update user's index """

        company_ids = list(
            map(lambda c: c.id, user.companies.all())
        )
        attachment = user.attachments.last()
        obj = cls(
            meta={'id': user.id},
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_ids=company_ids,
            attachment=attachment.full_urls() if attachment else None
        )
        obj.save()
        return obj.to_dict(include_meta=True)

# def rebuild_index():
#     """ Rebuild index for the users """
#
#     UserIndex.init()
#     users = User.objects.prefetch_related('companies', 'attachments')
#     for user in users:
#         print(UserIndex.store_index(user))
