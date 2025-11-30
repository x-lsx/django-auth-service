from .models import Role, RoleResourceAccess

def get_user_roles(user):
    if user.is_superuser:
        return ["superuser"]
    return list(
        user.user_roles.filter(is_active=True)
        .values_list("role__name", flat=True)
    )
    
def get_required_methods(permission_type):
    mapping = {
        "POST": ["can_create", None],
        "GET": ["can_read", "can_read_all"],
        "PATCH":  ["can_update", "can_update_all"],
        "PUT": ["can_update", "can_update_all"],
        "DELETE": ["can_delete", "can_delete_all"],
    }
    return mapping.get(permission_type, [])

def has_permission(user_roles, resource_code, required_permission: list[str]):
    if not user_roles or not resource_code:
        return False
    owner_perm, all_perm = required_permission
    
    access = RoleResourceAccess.objects.filter(
        role__name__in=user_roles,
        resource__code=resource_code).first()
    
    if not access:
        return False
    
    if all_perm and getattr(access, all_perm, False):
        return True
    if owner_perm and getattr(access, owner_perm, False):
        return True
    
    return False