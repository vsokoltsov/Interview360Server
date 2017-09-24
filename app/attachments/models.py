from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Attachment(models.Model):
    """ Uploaded file model representation """

    content_type = models.ForeignKey(ContentType, null=False)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    data = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
