from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text

class UserIndex(DocType):
    """ User class index """

    first_name = Text(analyzer='snowball')
    last_name = Text(analyzer='snowball')
    email = Text(analyzer='snowball')

    class Meta:
        index = 'users'
