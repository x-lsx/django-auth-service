
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .jwt_manager import verify_token
from apps.users.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        try:
            token = auth_header.split(" ", 1)[1]
        except IndexError:
            return None

        try:
            payload = verify_token(token, token_type="access")
            if not payload:
                return None

            user = User.objects.get(id=payload["user_id"])
            if not user.is_active:
                raise AuthenticationFailed("Пользователь не активен.")
            
            return (user, payload)
        except User.DoesNotExist:
            raise AuthenticationFailed("Пользователь не найден.")
        except Exception as e:
            raise AuthenticationFailed(f"Ошибка аутентификации: {str(e)}")

    def authenticate_header(self, request):
        return 'Bearer realm="api"'