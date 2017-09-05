from rest_framework.permissions import BasePermission
from roles.models import Candidate
from roles.constants import (
    RECEIVE_INTERVIEW, CREATE_INTERVIEW, UPDATE_INTERVIEW, DELETE_INTERVIEW
)
from companies.models import Company
import ipdb

class InterviewPermission(BasePermission):
    """ Permission class for InterviewViewSet class  """

    def has_permission(self, request, view):
        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = request.user.get_role_for_company(company)

        if view.action == 'list':
            return role.has_permission(RECEIVE_INTERVIEW)
        elif view.action == 'create':
            return role.has_permission(CREATE_INTERVIEW)
        else:
            return True

    def has_object_permission(self, request, view, obj=None):
        company = obj.vacancy.company
        role = request.user.get_role_for_company(company)
        if view.action == 'destroy' or request.method == 'DELETE':
            return role.has_permission(DELETE_INTERVIEW)
        elif view.action == 'update':
            return role.has_permission(UPDATE_INTERVIEW)
        elif view.action == 'retrieve':
            if type(role) == Candidate:
                return obj.candidate.id == request.user.id
            else:
                return role.has_permission(RECEIVE_INTERVIEW)
        else:
            return False
