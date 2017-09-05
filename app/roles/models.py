from django.db import models
from importlib import import_module
import ipdb
from .constants import *

def get_role(role):
    """ Receives user's role instance """

    try:
        module = import_module(__name__)
        return getattr(module, ROLE_IDENTIFIERS[role])()
    except KeyError:
        return None

class RoleManager:

    def has_permission(self, permission):
        """ Return boolean value for user access to operation """

        return permission in self.permissions

class Candidate(RoleManager):
    permissions = [
        RECEIVE_VACANCY,
        RECEIVE_INTERVIEW,
        RECEIVE_COMPANY
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
        RECEIVE_EMPLOYEES,
        DELETE_EMPLOYEES,
        ADD_EMPLOYEE_TO_COMPANY,
        CREATE_INTERVIEW,
        UPDATE_INTERVIEW,
        DELETE_INTERVIEW
    ]

class CompanyOwner(Hr):
    permissions = Hr.permissions + [
        UPDATE_COMPANY,
        DELETE_COMPANY
    ]
