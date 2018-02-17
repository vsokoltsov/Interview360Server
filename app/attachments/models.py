from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Attachment(models.Model):
    """ Uploaded file model representation """

    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType, null=False)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)

    def full_urls(self):
        """ Receive a hash of all available urls """

        url = self.data.url
        thumb_url = self.__get_url_by_type('thumb')
        small_thumb_url = self.__get_url_by_type('small_thumb')
        medium_url = self.__get_url_by_type('medium')
        medium_large_url = self.__get_url_by_type('medium_large')
        large_url = self.__get_url_by_type('large')

        return {
            'thumb_url': thumb_url,
            'small_thumb_url': small_thumb_url,
            'medium_url': medium_url,
            'medium_large_url': medium_large_url,
            'large_url': large_url
        }


    def __get_url_by_type(self, url_type):
        """ Return attachment url based on its type """

        return self.data[url_type].url


class Image(Attachment):
    """ Image implementation of attachment class """

    DEFAULT_SOURCE = 'data'
    DEFAULT_FORMAT = 'PNG'

    data = models.ImageField(upload_to='image')
    image_small_thumb = ImageSpecField(source=DEFAULT_SOURCE,
                                 processors=[ResizeToFill(50, 50)],
                                 format=DEFAULT_FORMAT)
    image_thumb = ImageSpecField(source=DEFAULT_SOURCE,
                                 processors=[ResizeToFill(100, 100)],
                                 format=DEFAULT_FORMAT)
    image_medium = ImageSpecField(source=DEFAULT_SOURCE,
                                 processors=[ResizeToFill(200, 200)],
                                 format=DEFAULT_FORMAT)
    image_medium_large = ImageSpecField(source=DEFAULT_SOURCE,
                                 processors=[ResizeToFill(250, 250)],
                                 format=DEFAULT_FORMAT)
    image_large = ImageSpecField(source=DEFAULT_SOURCE,
                                 processors=[ResizeToFill(350, 350)],
                                 format=DEFAULT_FORMAT)

    class Meta:
        db_table = 'attachment_images'
