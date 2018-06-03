from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Object


class UserIndex(DocType):
    """User class index."""

    id = Integer()
    first_name = Text()
    last_name = Text()
    email = Text()
    company_id = Integer()
    attachment = Object()

    class Meta:
        """Metaclass for index."""

        index = 'users'

    @classmethod
    def store_index(cls, user):
        """Create or update user's index."""

        company_ids = list(
            map(lambda c: c.id, user.companies.all())
        )
        attachment = user.avatars.last()
        obj = cls(
            meta={'id': user.id},
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_id=company_ids,
            attachment=attachment.full_urls() if attachment else None
        )
        obj.save()
        return obj.to_dict(include_meta=True)
