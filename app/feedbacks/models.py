from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from authorization.models import User

class Feedback(models.Model):
    """ Feedback model representations """

    ASSIGNED = 0
    IN_PROGRESS = 1
    DONE = 2

    STATUSES = [
        ASSIGNED,
        IN_PROGRESS,
        DONE
    ]

    STATUSES_NAMES = [
        'assigned',
        'in progress',
        'done'
    ]

    user = models.ForeignKey(User, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'feedbacks'

    @classmethod
    def status_value(cls, val):
        """ Get name of the status by status value """

        return cls.STATUSES_NAMES.index(val) if val in cls.STATUSES else None
