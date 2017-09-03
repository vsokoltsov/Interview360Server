from django.db import models
from django.apps import apps

ROLE_IDENTIFIERS = {
    '1': 'CompanyOwner',
    '2': 'Hr',
    '3': 'Candidate',
    '4': 'Employee'
}
CREATE_COMPANY = 'create_company'
UPDATE_COMPANY = 'update_company'
DELETE_COMPANY = 'delete_company'
ADD_EMPLOYEE_TO_COMPANY = 'add_employee_to_company'
RECEIVE_VACANCY = 'receive_vacancy'
CREATE_VACANCY = 'create_vacancy'
UPDATE_VACANCY = 'update_vacancy'
DELETE_VACANCY = 'delete_vacancy'
ADD_EMPLOYEE_TO_INTERVIEW = 'add_employee_to_interview'
RECEIVE_INTERVIEW = 'receive_interview'
CREATE_INTERVIEW = 'create_interview'
UPDATE_INTERVIEW = 'update_interview'
DELETE_INTERVIEW = 'delete_interview'
PARTICIPATE_INTERVIEW = 'participate_interview'
CREATE_FEEDBACK = 'create_feedback'
UPDATE_FEEDBACK = 'update_feedback'
DELETE_FEEDBACK = 'delete_feedback'

def get_role(role):
    try:
        return apps.get_model('roles', ROLE_IDENTIFIERS[role])
    except KeyError:
        return None

class RoleManager:

    def has_permission(self, permission):
        """ Return boolean value for user access to operation """

        return permission in permissions

class Candidate(RoleManager):
    permissions = [
        RECEIVE_VACANCY,
        RECEIVE_INTERVIEW
    ]

class Employee(Candidate):
    permissions = Candidate.permissions + [
        PARTICIPATE_INTERVIEW,
        CREATE_FEEDBACK,
        UPDATE_FEEDBACK,
        DELETE_FEEDBACK
    ]

class Hr(Employee):
    permissions = Employee.permissions + [
        CREATE_VACANCY,
        UPDATE_VACANCY,
        DELETE_VACANCY,
        ADD_EMPLOYEE_TO_INTERVIEW,
        ADD_EMPLOYEE_TO_COMPANY,
        CREATE_INTERVIEW,
        UPDATE_INTERVIEW,
        DELETE_INTERVIEW
    ]

class CompanyOwner(Hr):
    permissions = Hr.permissions + [
        CREATE_COMPANY,
        UPDATE_COMPANY,
        DELETE_COMPANY
    ]

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
