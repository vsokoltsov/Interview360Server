import factory
from datetime import datetime

class CompanyFactory(factory.django.DjangoModelFactory):
    """ Factory for the company model """

    class Meta:
        model = 'companies.Company'

    name = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('text')
    city = factory.Faker('address.city')
    start_date = factory.LazyFunction(datetime.now)
