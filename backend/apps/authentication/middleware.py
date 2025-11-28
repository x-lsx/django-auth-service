from django.utils.deprecation import MiddlewareMixin
from apps.authentication.jwt_manager import verify_token
from apps.users.models import User


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            request.user = None
            request.jwt_payload = None
            request.user_roles = []
            return None

        token = auth_header.split(" ")[1]

        payload = verify_token(token, token_type="access")

        if not payload:
            request.user = None
            request.jwt_payload = None
            request.user_roles = []
            return None

        try:
            user = User.objects.only("id", "is_active").get(id=payload["user_id"])
            if not user.is_active:
                raise User.DoesNotExist
        except User.DoesNotExist:
            
            request.user = None
            request.jwt_payload = None
            request.user_roles = []
            return None

        request.user = user
        request.jwt_payload = payload
        request.user_roles = payload.get("roles", [])

        return None