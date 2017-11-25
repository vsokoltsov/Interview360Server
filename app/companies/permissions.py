from rest_framework import permissions
from .models import Company, CompanyMember
from roles.constants import (
    COMPANY_OWNER, RECEIVE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY,
    RECEIVE_EMPLOYEES, ADD_EMPLOYEE_TO_COMPANY, DELETE_EMPLOYEES
)
from roles.models import get_role
import ipdb

class CompanyPermissions(permissions.BasePermission):
    """ Custom permission class; Check if user is company's owner """

    def has_permission(self, request, view):
        return True


    def has_object_permission(self, request, view, obj):

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
    """ Permissions for EmployeeViewSet """


    def has_permission(self, request, view, obj=None):
        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = request.user.get_role_for_company(company)

        if request.method == 'PUT': return True


        if view.action == 'list':
            return role.has_permission(RECEIVE_EMPLOYEES)
        if view.action == 'retrieve':
            return role.has_permission(RECEIVE_EMPLOYEES)
        elif request.user.is_activated_for_company(company) and view.action == 'create':
            return role.has_permission(ADD_EMPLOYEE_TO_COMPANY)
        elif request.user.is_activated_for_company(company) and view.action == 'destroy':
            return role.has_permission(DELETE_EMPLOYEES)
        elif view.action == 'search':
            return role.has_permission(RECEIVE_EMPLOYEES)
        else:
            return False
