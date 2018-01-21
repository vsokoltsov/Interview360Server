from django.db import models

class Resume(models.Model):
    """ Resume representation in the system """

    user = models.ForeignKey('authorization.User', null=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    skills = models.ManyToManyField('skills.Skill')
    salary = models.DecimalField(max_digits=8, decimal_places=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resumes'

class Workplace(models.Model):
    """ Workplace representation in the system """

    company = models.ForeignKey('companies.Company', null=False)
    resume = models.ForeignKey('resumes.Resume', null=False, related_name='workplaces')
    position = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workplaces'
