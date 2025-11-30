from django.urls import path
from .views import RefreshTokenView, RegisterView, LoginView, LogoutView, UserUpdateView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('profile/update/', UserUpdateView.as_view(), name='user-update'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]