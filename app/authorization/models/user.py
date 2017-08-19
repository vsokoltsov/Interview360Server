from . import AbstractBaseUser, BaseUserManager
from . import models

class User(AbstractBaseUser):
    """ Represents a user object in our system """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    companies = models.ManyToManyField('companies.Company', through='companies.CompanyMember')

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """ String representation of user """

        return self.email

    class Meta:
        db_table = 'users'
