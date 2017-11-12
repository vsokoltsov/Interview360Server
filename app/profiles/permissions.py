from rest_framework import permissions
import ipdb

class UserProfilePermission(permissions.BasePermission):
    """ Permissions for accessing to user profile """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if view.action == 'retrieve':
            return True
        elif view.action == 'update' and current_user.id == obj.id:
            return True
        elif view.action == 'change_password' and current_user.id == obj.id:
            return True
        elif view.action == 'destroy' and current_user.id == obj.id:
            return True
        else:
            return False
