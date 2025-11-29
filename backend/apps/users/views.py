from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import AllowAny

from .serializers import UserLoginSerializer, UserProfileSerializer, UserRegisterSerializer, UserUpdateSerializer
from ..authentication.jwt_manager import generate_jwt, verify_token, refresh_tokens, revoke_token


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserProfileSerializer(user).data,
            "tokens": generate_jwt(user)
        }, status=status.HTTP_201_CREATED)
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        return Response({
            "user": UserProfileSerializer(user).data,
            "tokens": generate_jwt(user)
        })
        
class LogoutView(APIView):
    permission_classes = []

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Уже вышли"}, status=400)

        jti = request.auth.get("jti")
        exp = request.auth.get("exp")

        if jti and exp:
            revoke_token(jti, exp)

        return Response({"detail": "Успешно вышли из системы."})
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh-токен обязателен."},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_tokens = refresh_tokens(refresh_token)
        if not new_tokens:
            return Response(
                {"detail": "Неверный или отозванный refresh-токен."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "tokens": new_tokens,
            "detail": "Токены успешно обновлены."
        })

class UserProfileView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)