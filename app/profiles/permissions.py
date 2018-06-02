from rest_framework import permissions
import ipdb


class UserProfilePermission(permissions.BasePermission):
    """Permissions for accessing to user profile."""

    def has_permission(self, request, view):
        """Return base entity permissions."""

        return True

    def has_object_permission(self, request, view, obj):
        """Return particular object permissions."""

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
