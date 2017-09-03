from rest_framework import permissions
from .models import Company, CompanyMember
from roles.constants import (
    COMPANY_OWNER, RECEIVE_COMPANY, DELETE_COMPANY, UPDATE_COMPANY
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
            return False
