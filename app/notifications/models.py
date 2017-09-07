from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from authorization.models import User

class Notification(models.Model):
    """ Notification representation in the system """

    user = models.ForeignKey(User, null=False)
    active = models.BooleanField(default=True)
    type = models.IntegerField(
        null=False,
        validators=[MaxValueValidator(2), MinValueValidator(1)]
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
