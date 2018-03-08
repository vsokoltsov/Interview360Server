import factory
from datetime import datetime
from roles.constants import EMPLOYEE

class CompanyFactory(factory.django.DjangoModelFactory):
    """ Factory for the company model """

    class Meta:
        model = 'companies.Company'

    name = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('text')
    city = factory.Faker('address')
    start_date = factory.LazyFunction(datetime.now)


class CompanyMemberFactory(factory.django.DjangoModelFactory):
    """ Factory for the company member model """

    class Meta:
        model = 'companies.CompanyMember'

    active = True
    role = EMPLOYEE
