from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from easy_thumbnails.fields import ThumbnailerField

class Attachment(models.Model):
    """ Uploaded file model representation """

    class Meta:
        db_table = 'attachments'

    content_type = models.ForeignKey(ContentType, null=False)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    data = ThumbnailerField()

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
