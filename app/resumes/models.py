from django.db import models

class Resume(models.Model):
    """ Resume representation in the system """

    user = models.ForeignKey('authorization.User', null=False)
    description = models.TextField()
    skills = models.ManyToManyField('skills.Skill')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
