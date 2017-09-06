from django.db import models
from vacancies.models import Vacancy
from authorization.models import User
from django.contrib.contenttypes.fields import GenericRelation

class Interview(models.Model):
    """ Interview object representation """

    vacancy = models.ForeignKey(Vacancy, null=False, related_name='interviews')
    candidate = models.ForeignKey(User, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    passed = models.NullBooleanField()
    assigned_at = models.DateTimeField(auto_now=True)

    interviewees = models.ManyToManyField(
        'authorization.User',
        through='InterviewEmployee',
        related_name='interviewees'
    )
    feedbacks = GenericRelation('feedbacks.Feedback')


    class Meta:
        db_table = 'interviews'

class InterviewEmployee(models.Model):
    """ Intermediate table among the Interview, User and Role """

    employee = models.ForeignKey(User, null=False)
    interview = models.ForeignKey(Interview, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interview_employees'
