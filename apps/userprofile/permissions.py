from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Permission of is owner only"""

    def has_object_permission(self, request, view, obj):
        return bool(
            obj == request.user
        )
