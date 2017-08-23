from django.db import models

# Create your models here.
class Vacancy(models.Model):
    """ Vacancy representation in our system """

    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    salary = models.DecimalField(max_digits=5, decimal_places=3, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vacancies'
