from django.db import models
from apps.users.models import User


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.name
    
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
    
class Resource(models.Model):
    code = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

class RoleResourceAccess(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    
    can_create = models.BooleanField(default=False)

    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
        
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'resource')

    def __str__(self):
        return f"{self.role.name} - {self.resource.name}"