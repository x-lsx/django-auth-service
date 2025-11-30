from rest_framework import serializers

from .models import Role, UserRole, Resource, RoleResourceAccess

class RoleSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "description", "users_count"]
        read_only_fields = ["id"]

    def get_users_count(self, obj):
        return obj.user_roles.filter(is_active=True).count()

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'code', 'name', 'description']
        read_only_fields = ['id']

class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = UserRole
        fields = [
            "id",
            "user_id",
            "user_email",
            "role",
            "is_active",
            "assigned_at",
        ]
        read_only_fields = ["id", "assigned_at"]
        
class UserRoleCreateSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(),
                                                source="role", write_only=True)
    class Meta:
        model = UserRole
        fields = ["user", "role_id", "is_active"]
        read_only_fields = ["assigned_at"]
        
class RoleResourceAccessSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True)
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(), source="resource", write_only=True)

    class Meta:
        model = RoleResourceAccess
        fields = [
            "id",
            "role",
            "role_id",
            "resource",
            "resource_id",
            "can_create",
            "can_read",
            "can_read_all",
            "can_update",
            "can_update_all",
            "can_delete",
            "can_delete_all",
        ]
        read_only_fields = ["id"]
        
