from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    message = "Admin privileges required."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        role = getattr(user, "role", None)
        return bool(
            role == "admin"
            or getattr(user, "is_staff", False)
            or getattr(user, "is_superuser", False)
        )
