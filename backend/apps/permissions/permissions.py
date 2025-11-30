from rest_framework import permissions
from .services import get_user_roles, get_required_methods, has_permission
from .models import Resource

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if getattr(view, "is_public", False):
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        resource_code = getattr(view, "resource_code", None)
        if not resource_code:
            return False

        try:
            Resource.objects.get(code=resource_code)
        except Resource.DoesNotExist:
            return False

        user_roles = get_user_roles(request.user)
        required = get_required_methods(request.method)

        if not required:
            return False

        return has_permission(user_roles, resource_code, required)