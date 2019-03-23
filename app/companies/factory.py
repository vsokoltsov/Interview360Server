import factory
from datetime import datetime
from roles.constants import EMPLOYEE


class CompanyFactory(factory.django.DjangoModelFactory):
    """Factory for the company model."""

    class Meta:
        """Factory's metaclass."""

        model = 'companies.Company'

    name = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('text')
    city = factory.Faker('city')
    country = factory.Faker('country')
    start_date = factory.LazyFunction(datetime.now)


class CompanyMemberFactory(factory.django.DjangoModelFactory):
    """Factory for the company member model."""

    class Meta:
        """Factory's metaclass."""

        model = 'companies.CompanyMember'

    active = True
    role = EMPLOYEE


class SpecialtyFactory(factory.django.DjangoModelFactory):
    """Factory for the specialty model."""

    class Meta:
        """Factory's metaclass."""

        model = 'companies.Specialty'

    name = factory.Faker('sentence', nb_words=2)
