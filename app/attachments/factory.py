import factory
from datetime import datetime

class ImageFactory(factory.django.DjangoModelFactory):
    """ Factory for the attachment model """

    class Meta:
        model = 'attachments.Image'

    data = factory.django.ImageField(color='blue')
