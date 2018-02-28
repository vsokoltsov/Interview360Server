from rest_framework import permissions
from .models import Resume

from roles.constants import (
    COMPANY_OWNER, RECEIVE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY,
    RECEIVE_EMPLOYEES, ADD_EMPLOYEE_TO_COMPANY, DELETE_EMPLOYEES
)
from roles.models import get_role

class ResumePermissions(permissions.BasePermission):
    """ Permission class for the resumes """

    def has_permission(self, request, view):
        """ Base permissions handler """

        return True

    def has_object_permission(self, request, view, obj):
        """ Object permissions handler """

        if view.action == 'update' or view.action == 'destroy':
            return request.user.id == obj.user_id
        else:
            return True
