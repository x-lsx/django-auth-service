from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
import uuid
import jwt

from apps.users.models import User

def generate_jwt(user: User) -> dict:
    """генерация access и refresh токенов для пользователя"""
    if not user or not user.is_active:
        raise ValidationError("Пользователь не активен")
    
    now = datetime.now(timezone.utc)
    
    access_payload = {
        'user_id': user.id,
        'roles': user.get_role_names(),
        'exp': now + timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES),
        'iat': now,
        "jti": str(uuid.uuid4()),
        'token_type': 'access'
    }
    refresh_payload = {
        'user_id': user.id,
        'exp': now + timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS),
        'iat': now,
        "jti": str(uuid.uuid4()),
        'token_type': 'refresh'
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return {
        "access": access_token,
        "refresh": refresh_token
    }
def verify_token(token: str, token_type: str = 'access') -> Optional[Dict]:
    """Верификация токена"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )
        if payload.get('token_type') != token_type:
            return None

        jti = payload.get('jti')
        if jti and is_token_revoked(jti):
            return None

        return payload
        
    except jwt.ExpiredSignatureError:
        raise ValidationError("Токен истек")
    except jwt.InvalidTokenError as e:
        raise ValidationError(f"Невалидный токен: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Ошибка верификации токена: {str(e)}")

def refresh_tokens(refresh_token: str) -> Optional[Dict[str, str]]:
    """обновление access и refresh токенов с использованием refresh токена"""
    try:
        payload = verify_token(refresh_token, 'refresh')
        if not payload:
            return None
        
        user_id = payload.get('user_id')
        user = User.objects.filter(id=user_id, is_active=True).first()
        
        if not user:
            return None
        
        revoke_token(payload['jti'], payload['exp'])
        
        return generate_jwt(user)
        
    except ValidationError:
        return None

def revoke_token(jti: str, exp: int) -> None:
    """отзыв токена путем добавления его jti в черный список"""
    ttl = exp - int(datetime.now(timezone.utc).timestamp())
    if ttl > 0:
        cache.set(f"revoked_jti_{jti}", True, timeout=ttl)

def is_token_revoked(jti: str) -> bool:
    """проверка, отозван ли токен по его jti"""
    return cache.get(f"revoked_jti_{jti}") is not None