from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrIsAuthenticated(BasePermission):
    """Permission of is owner or staff for editing"""

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.owner == request.user or
            request.user.is_staff
        )