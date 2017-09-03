from django.db import models

ROLE_IDENTIFIERS = {
    '1': 'AuthorizedUser',
    '2': 'CompanyOwner',
    '3': 'Hr',
    '4': 'Candidate',
    '5': 'Employee'
}

def get_user_role_in_company():
    pass  

class AuthorizedUser:
    pass

class CompanyOwner:
    pass

class Hr:
    pass

class Candidate:
    pass

class Employee:
    pass

class Role(models.Model):
    """ User's roles representation """

    # TODO
    # - rethink the role mechanism
    # - possible solutions:
    #   1 Add role_name to CompanyMember instance where employee can specify
    #       his role in the company. `role_id` field will point at his
    #       permissions level
    #   2 Add boolean field for any particular operation
    #       allowed (or not allowed) to user
    #   3 Implement STI for roles and create new instances for every
    #       company_member instance (same as the 1)

    class Meta:
        db_table = 'roles'

    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
