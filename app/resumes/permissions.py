from rest_framework import permissions
from .models import Resume

from roles.constants import (
    COMPANY_OWNER, RECEIVE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY,
    RECEIVE_EMPLOYEES, ADD_EMPLOYEE_TO_COMPANY, DELETE_EMPLOYEES
)
from roles.models import get_role
import ipdb

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

class ContactPermissions(permissions.BasePermission):
    """ Permissions class for resume's contact """

    def has_permission(self, request, view):
        """ Base permissions handler """

        try:
            resume = Resume.objects.get(id=view.kwargs.get('resume_id'))
            return request.user.id == resume.user_id
        except Resume.DoesNotExist:
            return True

class WorkplacePermissions(permissions.BasePermission):
    """ Permissions class for resume's workplaces """

    def has_permission(self, request, view, resume_id=None):
        """ Base permissions handler """

        try:
            resume = Resume.objects.get(id=view.kwargs.get('resume_id'))
            return request.user.id == resume.user_id
        except Resume.DoesNotExist:
            return True
