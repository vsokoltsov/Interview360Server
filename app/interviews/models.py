from django.db import models
from vacancies.models import Vacancy
from authorization.models import User
# Create your models here.

class Interview(models.Model):
    """ Interview object representation """

    vacancy = models.ForeignKey(Vacancy, null=False)
    candidate = models.ForeignKey(User, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interviews'
