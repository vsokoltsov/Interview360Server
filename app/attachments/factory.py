import factory
from datetime import datetime


class ImageFactory(factory.django.DjangoModelFactory):
    """Factory for the attachment model."""

    class Meta:
        """Factory's metaclass."""

        model = 'attachments.Image'

    data = factory.django.ImageField(color='blue')
