from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Permission of is owner or staff for editing"""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj.user == request.user or
            request.user.is_staff
        )


class IsOwnerOrStaff(BasePermission):
    """Permission of is owner or staff"""

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user == request.user or
            request.user.is_staff
        )
