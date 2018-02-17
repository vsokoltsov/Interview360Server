from . import (
    models, AbstractBaseUser, GenericRelation,
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
    feedbacks = GenericRelation('feedbacks.Feedback')
    avatars = GenericRelation('attachments.Image')

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    def get_role_for_company(self, company):
        """ Return user's role in the company """

        company_member_class = apps.get_model('companies', 'CompanyMember')
        role = company_member_class.objects.get(
            user_id=self.id, company_id=company.id
        ).role
        return get_role(str(role))

    def has_role(self, company, role_id):
        """ Return matching user's role in company to specific role """

        company_member_class = apps.get_model('companies', 'CompanyMember')
        role = company_member_class.objects.get(
            user_id=self.id, company_id=company.id
        ).role
        return int(role) == int(role_id)

    def is_activated_for_company(self, company):
        """ Returns whether or not user is active in company """

        company_member_class = apps.get_model('companies', 'CompanyMember')
        try:
            return company_member_class.objects.get(
                user_id=self.id, company_id=company.id
            ).active
        except company_member_class.DoesNotExist:
            return False

    def get_roles_for_companies(self):
        """
        Return dictionary of company id's with role id's
        """

        return {
            item.company_id: item.role for item in  self.companymember_set.all()
        }

    def __str__(self):
        """ String representation of user """

        return self.email

    class Meta:
        db_table = 'users'
