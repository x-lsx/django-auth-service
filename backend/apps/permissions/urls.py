from django.urls import path
from .views import (RoleListCreateView, RoleDetailView, ResourceListCreateView,
                    RoleResourceAccessListCreateView, RoleResourceAccessDetailView,
                    UserRoleListCreateView)
urlpatterns = [
    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list'),
    path('role-resource-access/', RoleResourceAccessListCreateView.as_view(), name='role-resource-access'),
    path('role-resource-access/<int:pk>/', RoleResourceAccessDetailView.as_view(), name='role-resource-access-detail'),    
    path('user-roles/', UserRoleListCreateView.as_view(), name='user-role-list-create'),
]