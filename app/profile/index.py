from authorization.models import User
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text

class UserIndex(DocType):
    """ User class index """

    first_name = Text(analyzer='snowball')
    last_name = Text(analyzer='snowball')
    email = Text(analyzer='snowball')

    class Meta:
        index = 'users'

def rebuild_index():
    """ Rebuild index for the users """

    for user in User.objects.all().iterator():
        obj = UserIndex(
            meta={'id': user.id},
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
        obj.save()
        print(obj.to_dict(include_meta=True))
