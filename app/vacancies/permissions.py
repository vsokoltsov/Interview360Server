from rest_framework.permissions import BasePermission
from companies.models import Company
from roles.constants import (
    RECEIVE_VACANCY, CREATE_VACANCY, UPDATE_VACANCY, DELETE_VACANCY
)
import ipdb


class VacancyPermission(BasePermission):
    """Permission class for VacancyViewSet."""

    def has_permission(self, request, view):
        """Return base entity permission."""

        user = request.user
        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = user.get_role_for_company(company)
        if view.action == 'list':
            return role.has_permission(RECEIVE_VACANCY)
        elif (view.action == 'create' and
              user.is_activated_for_company(company)):
            return role.has_permission(CREATE_VACANCY)
        elif view.action == 'search':
            return role.has_permission(RECEIVE_VACANCY)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        """Return particular object permission."""

        user = request.user
        company = obj.company
        role = user.get_role_for_company(company)
        if view.action == 'retrieve':
            return role.has_permission(RECEIVE_VACANCY)
        elif (view.action == 'create' and
              user.is_activated_for_company(company)):
            return role.has_permission(CREATE_VACANCY)
        elif (view.action == 'destroy' and
              user.is_activated_for_company(company)):
            return role.has_permission(DELETE_VACANCY)
        else:
            return False
