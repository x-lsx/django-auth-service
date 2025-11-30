# apps/permissions/admin.py
from django.contrib import admin
from .models import Role, UserRole, Resource, RoleResourceAccess


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "users_count", "description")
    search_fields = ("name",)
    ordering = ("name",)

    def users_count(self, obj):
        return obj.user_roles.filter(is_active=True).count()
    users_count.short_description = "Пользователей"


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user_email", "role", "is_active", "assigned_at")
    list_filter = ("is_active", "role", "assigned_at")
    search_fields = ("user__email", "role__name")
    raw_id_fields = ("user",)
    ordering = ("-assigned_at",)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"
    user_email.admin_order_field = "user__email"


@admin.register(RoleResourceAccess)
class RoleResourceAccessAdmin(admin.ModelAdmin):
    list_display = (
        "role", "resource", 
        "can_create", "can_read", "can_read_all",
        "can_update", "can_update_all",
        "can_delete", "can_delete_all"
    )
    list_filter = ("role", "resource", "can_read_all", "can_update_all", "can_delete_all")
    search_fields = ("role__name", "resource__code")
    ordering = ("role__name", "resource__code")

    # Красивые булевы иконки
    def has_permission_icon(self, obj, perm):
        return "Да" if getattr(obj, perm, False) else "—"
    
    for perm in ["can_create", "can_read", "can_read_all", "can_update", "can_update_all", "can_delete", "can_delete_all"]:
        locals()[perm] = lambda self, obj, p=perm: self.has_permission_icon(obj, p)
        locals()[perm].short_description = perm.replace("can_", "").replace("_", " ").title()