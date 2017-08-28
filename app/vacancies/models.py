from django.db import models
from companies.models import Company
from skills.models import Skill

# Create your models here.
class Vacancy(models.Model):
    """ Vacancy representation in our system """

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    salary = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('companies.Company', null=False)

    skills = models.ManyToManyField('skills.Skill', through='vacancies.VacancySkill')

    class Meta:
        db_table = 'vacancies'

class VacancySkill(models.Model):
    """ Throught table for vacancies and skills """

    class Meta:
        auto_created = True
        db_table = 'vacancy_skills'

    vacancy = models.ForeignKey(Vacancy)
    skill = models.ForeignKey(Skill)
