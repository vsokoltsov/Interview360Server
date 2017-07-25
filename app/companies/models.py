from django.db import models
from authorization.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    start_date = models.DateField(null=False)
    description = models.TextField()
    city = models.CharField(null=False, max_length=255)
    founder = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
