from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    start_date = models.DateField(null=False)
    description = models.TextField()
    city = models.CharField(null=False, max_length=255)
