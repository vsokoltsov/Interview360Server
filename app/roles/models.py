from django.db import models

class Role(models.Model):
    """ User's roles representation """

    class Meta:
        db_table = 'roles'

    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
