from rest_framework import permissions
from .models import Company, CompanyMember
from roles.constants import (
    COMPANY_OWNER, HR, RECEIVE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY,
    RECEIVE_RESUME, CREATE_RESUME, RECEIVE_EMPLOYEES, ADD_EMPLOYEE_TO_COMPANY,
    DELETE_EMPLOYEES
)
from roles.models import get_role
import ipdb


class CompanyPermissions(permissions.BasePermission):
    """Custom permission class; Check if user is company's owner."""

    def has_permission(self, request, view):
        """Return base permission."""

        return True

    def has_object_permission(self, request, view, obj):
        """Return permission for object."""

        role = request.user.get_role_for_company(obj)
        if view.action == 'retrieve':
            return role.has_permission(RECEIVE_COMPANY)
        elif view.action == 'destroy':
            return role.has_permission(DELETE_COMPANY)
        elif view.action == 'update':
            return role.has_permission(UPDATE_COMPANY)
        else:
            return True


class EmployeePermission(permissions.BasePermission):
    """Permissions for EmployeeViewSet."""

    def has_permission(self, request, view, obj=None):
        """Return base permission."""

        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = request.user.get_role_for_company(company)

        if request.method == 'PUT':
            return True

        if request.user.is_activated_for_company(
                company) and view.action == 'list':
            return role.has_permission(RECEIVE_EMPLOYEES)
        if request.user.is_activated_for_company(
                company) and view.action == 'retrieve':
            return role.has_permission(RECEIVE_EMPLOYEES)
        elif (request.user.is_activated_for_company(company) and
              view.action == 'create'):
            return role.has_permission(ADD_EMPLOYEE_TO_COMPANY)
        elif (request.user.is_activated_for_company(company) and
              view.action == 'destroy'):
            return role.has_permission(DELETE_EMPLOYEES)
        elif view.action == 'search':
            return role.has_permission(RECEIVE_EMPLOYEES)
        else:
            return False
