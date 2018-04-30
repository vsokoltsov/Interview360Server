from rest_framework.permissions import BasePermission
from companies.models import Company
from roles.constants import (
    RECEIVE_FEEDBACK, CREATE_FEEDBACK, UPDATE_FEEDBACK, DELETE_FEEDBACK,
    HR, COMPANY_OWNER
)
from roles.models import Hr, Employee,


class FeedbackPermission(BasePermission):
    """ Permission class for the FeedbackViewSet """

    def has_permission(self, request, view):
        company = Company.objects.get(id=view.kwargs['company_pk'])
        role = request.user.get_role_for_company(company)

        if view.action == 'list':
            return role.has_permission(RECEIVE_FEEDBACK)
        elif view.action == 'create':
            return role.has_permission(CREATE_FEEDBACK)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        company = Company.objects.get(id=view.kwargs['company_pk'])
        user = request.user
        role = user.get_role_for_company(company)

        if view.action == 'retrieve':
            if obj.user_id == user.id:
                return True
            else:
                return role.has_permission(RECEIVE_FEEDBACK)
        elif view.action == 'destroy':
            if obj.user_id == user.id:
                return True
            else:
                return role.has_permission(DELETE_FEEDBACK)
        elif view.action == 'update':
            if obj.user_id == user.id:
                return True
            else:
                return role.has_permission(UPDATE_FEEDBACK)
        else:
            return False
