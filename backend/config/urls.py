from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/permissions/', include('apps.permissions.urls')),
    path('api/social/', include('apps.social.urls')),
]
