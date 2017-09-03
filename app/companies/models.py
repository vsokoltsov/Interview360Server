from django.db import models
from authorization.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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

    def get_employees_with_role(self, role_id):
        """
        Return list of employees who are belonging to the company
        and have the pointed role
        """

        return CompanyMember.objects.filter(
                company_id=self.id, role=role_id
            ).prefetch_related('user')

class CompanyMember(models.Model):
    """ CompanyMember model, which is used for `through` association """

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    role = models.IntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_members'
        index_together = unique_together = [
            ['user', 'company']
        ]
