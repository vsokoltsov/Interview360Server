from django.db import models
from vacancies.models import Vacancy
from authorization.models import User
from roles.models import Role
# Create your models here.

class Interview(models.Model):
    """ Interview object representation """

    vacancy = models.ForeignKey(Vacancy, null=False)
    candidate = models.ForeignKey(User, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    interviewees = models.ManyToManyField('authorization.User', through='InterviewEmployee', related_name='interviewees')

    class Meta:
        db_table = 'interviews'

class InterviewEmployee(models.Model):
    """ Intermediate table among the Interview, User and Role """

    employee = models.ForeignKey(User, null=False)
    interview = models.ForeignKey(Interview, null=False)
    role = models.ForeignKey(Role, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interview_employees'
