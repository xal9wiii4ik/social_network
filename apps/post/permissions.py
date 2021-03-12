from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Permission of is owner or staff for editing"""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj.owner == request.user
        )


class IsAdminOrReadOnly(BasePermission):
    """Permission of is read only or admin for editing"""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user.is_authenticated
        )


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """Permission of is owner or staff or read only"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS and
            request.user.is_authenticated or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated or
            obj.owner == request.user or
            request.user.is_staff
        )
