from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import RoleSerializer, UserRoleCreateSerializer, UserRoleSerializer, ResourceSerializer, RoleResourceAccessSerializer
from .models import Role, UserRole, Resource, RoleResourceAccess
from .permissions import CustomPermission


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CustomPermission]
    resource_code = "roles"
    
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CustomPermission]
    resource_code = "roles"
    
class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [CustomPermission]
    resource_code = "resources"
    
class RoleResourceAccessListCreateView(generics.ListCreateAPIView):
    queryset = RoleResourceAccess.objects.all()
    serializer_class = RoleResourceAccessSerializer
    permission_classes = [CustomPermission]
    resource_code = "role_resource_accesses"
    
class RoleResourceAccessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleResourceAccess.objects.all()
    serializer_class = RoleResourceAccessSerializer
    permission_classes = [CustomPermission]
    resource_code = "role_resource_accesses"

class UserRoleListCreateView(generics.ListCreateAPIView):
    queryset = UserRole.objects.select_related("user", "role")
    permission_classes = [CustomPermission]
    resource_code = "user_roles"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRoleCreateSerializer
        return UserRoleSerializer    

    


