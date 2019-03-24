from django.db import models
from companies.models import Company
from skills.models import Skill


class Vacancy(models.Model):
    """Vacancy representation in our system."""

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    salary = models.DecimalField(max_digits=6, decimal_places=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        'companies.Company',
        null=False, on_delete=models.PROTECT
    )
    active = models.BooleanField(default=True)

    skills = models.ManyToManyField(Skill)

    class Meta:
        """Model's metaclass."""

        db_table = 'vacancies'
