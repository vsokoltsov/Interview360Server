from django.db import models
from authorization.models import User
# Create your models here.

class Company(models.Model):
    """ Base company model """

    name = models.CharField(max_length=255, null=False)
    start_date = models.DateField(null=False)
    description = models.TextField()
    city = models.CharField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    employees = models.ManyToManyField('authorization.User', through='CompanyMember')

    class Meta:
        db_table = 'companies'

class CompanyMember(models.Model):
    """ CompanyMember model, which is used for `through` association """

    ROLES = [
        'owner',
        'hr',
        'employee'
    ]

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    role = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_members'
