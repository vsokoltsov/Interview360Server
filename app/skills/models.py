from django.db import models

# Create your models here.
class Skill(models.Model):
    """ Employee's skills representation """

    class Meta:
        db_table = 'skills'

    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
