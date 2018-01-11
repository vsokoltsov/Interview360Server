from elasticsearch_dsl import (
    DocType, Date, Float, Integer, Boolean, Keyword, Text, Object
)

class ResumesIndex(DocType):
    """ Resumes index class """

    id = Integer()
    title = Text(analyzer='standard')
    description = Text(analyzer='standard')
    skills = Keyword()
    user = Text(analyzer='standard')
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = 'resumes'
