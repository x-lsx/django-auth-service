# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_superuser", "date_joined")
    list_filter = ("is_active", "is_superuser", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Персональная информация"), {"fields": ("first_name", "last_name", "middle_name")}),
        (_("Статус"), {"fields": ("is_active", "is_superuser")}),
        (_("Даты"), {"fields": ("date_joined", "updated_at", "deleted_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_superuser"),
        }),
    )
    
    readonly_fields = ("date_joined", "updated_at", "deleted_at")
    
    # Показываем роли прямо в профиле пользователя
    def user_roles_display(self, obj):
        return ", ".join([ur.role.name for ur in obj.user_roles.filter(is_active=True)])
    user_roles_display.short_description = "Роли"
    
    list_display += ("user_roles_display",)