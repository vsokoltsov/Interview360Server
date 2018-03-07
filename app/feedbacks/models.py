from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from authorization.models import User

class Feedback(models.Model):
    """ Feedback model representations """

    ASSIGNED = 0
    IN_PROGRESS = 1
    DONE = 2

    STATUSES = (
        (ASSIGNED, 'Assigned'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done')
    )

    user = models.ForeignKey(User, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.IntegerField(
        null=False, default=ASSIGNED, choices=STATUSES, db_index=True
    )

    class Meta:
        db_table = 'feedbacks'
