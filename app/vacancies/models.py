from django.db import models
from companies.models import Company

# Create your models here.
class Vacancy(models.Model):
    """ Vacancy representation in our system """

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    salary = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('companies.Company', null=False)

    class Meta:
        db_table = 'vacancies'
