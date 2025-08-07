from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.utils.config import settings


# Utility class for working with JWT tokens
class JWTUtils:

    @staticmethod
    def create_access_token(data: dict, expires_minutes: int = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return {
                "username": payload.get("sub"),
                "role": payload.get("role")
            }
        except JWTError:
            return None
