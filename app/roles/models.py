from django.db import models
from importlib import import_module
from .constants import *


def get_role(role):
    """Receives user's role instance."""

    try:
        module = import_module(__name__)
        return getattr(module, ROLE_IDENTIFIERS[role])()
    except KeyError:
        return None


class RoleManager:
    """Base role manager class."""

    def has_permission(self, permission):
        """Return boolean value for user access to operation."""

        return permission in self.permissions


class Candidate(RoleManager):
    """Candidate role class."""

    permissions = [
        RECEIVE_VACANCY,
        RECEIVE_INTERVIEW,
        RECEIVE_COMPANY,
        RECEIVE_RESUME,
        CREATE_RESUME,
        UPDATE_RESUME,
        DELETE_RESUME
    ]


class Employee(Candidate):
    """Employee role class."""

    permissions = Candidate.permissions + [
        PARTICIPATE_INTERVIEW,
        RECEIVE_FEEDBACK,
        CREATE_FEEDBACK,
        UPDATE_FEEDBACK,
        DELETE_FEEDBACK
    ]


class Hr(Employee):
    """Hr role class."""

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
    """Company owner role class."""

    permissions = Hr.permissions + [
        UPDATE_COMPANY,
        DELETE_COMPANY
    ]
