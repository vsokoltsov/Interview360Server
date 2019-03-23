import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Factory object for the user model."""

    class Meta:
        """Metaclass for factory."""

        model = 'authorization.User'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(
        a.first_name, a.last_name).lower()
    )
