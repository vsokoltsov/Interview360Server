from django.db import models
from authorization.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from .managers import CompanyManager

class Company(models.Model):
    """ Base company model """

    name = models.CharField(max_length=255, null=False)
    start_date = models.DateField(null=True)
    description = models.TextField()
    city = models.CharField(null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    employees = models.ManyToManyField('authorization.User', through='CompanyMember')
    images = GenericRelation('attachments.Image')
    specialties = models.ManyToManyField('companies.Specialty')
    objects = CompanyManager()

    class Meta:
        db_table = 'companies'

    def get_employees_with_role(self, role):
        """
        Return list of employees who are belonging to the company
        and have the pointed role
        """

        objects = CompanyMember.objects.filter(
                company_id=self.id, role=role
            ).prefetch_related('user')
        return list(map(lambda member: member.user, objects))

    @classmethod
    def prefetch_for_list(cls):
        objects = cls.objects.prefetch_related(
            'vacancy_set', 'images', 'employees'
        )
        objects = (
            objects
                .annotate(Count('employees', distinct=True))
                .annotate(Count('vacancy', distinct=True))
        )
        return objects

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

class Specialty(models.Model):
    """ Specialty of the company model """

    class Meta:
        db_table = 'specialties'

    name = name = models.CharField(max_length=255, null=False, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
