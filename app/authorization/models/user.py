from . import (
    models, AbstractBaseUser,
    BaseUserManager, apps, get_role
)

class User(AbstractBaseUser):
    """ Represents a user object in our system """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    companies = models.ManyToManyField('companies.Company', through='companies.CompanyMember')
    interviews = models.ManyToManyField('interviews.Interview', through='interviews.InterviewEmployee')

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    def get_role_for_company(self, company):
        """ Return user's role in the company """

        company_member_class = apps.get_model('companies', 'CompanyMember')
        role = company_member_class.objects.get(
            user_id=self.id, company_id=company.id
        ).role
        return get_role(str(role))

    def __str__(self):
        """ String representation of user """

        return self.email

    class Meta:
        db_table = 'users'
