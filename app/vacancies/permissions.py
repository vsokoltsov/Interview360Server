from rest_framework.permissions import BasePermission
from companies.models import Company
from roles.constants import (
    RECEIVE_VACANCY, CREATE_VACANCY, UPDATE_VACANCY, DELETE_VACANCY
)
import ipdb

class VacancyPermission(BasePermission):
    """ Permission class for VacancyViewSet """

    def has_permission(self, request, view):
        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = request.user.get_role_for_company(company)
        if view.action == 'list':
            return role.has_permission(RECEIVE_VACANCY)
        elif view.action == 'create':
            return role.has_permission(CREATE_VACANCY)
        elif view.action == 'search':
            return role.has_permission(RECEIVE_VACANCY)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        company = obj.company
        role = request.user.get_role_for_company(company)
        if view.action == 'retrieve':
            return role.has_permission(RECEIVE_VACANCY)
        elif view.action == 'create':
            return role.has_permission(CREATE_VACANCY)
        elif view.action == 'destroy':
            return role.has_permission(DELETE_VACANCY)
        else:
            return False
