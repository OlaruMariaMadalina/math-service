from fastapi import Request
from typing import Optional, Tuple
from app.auth.jwt_utils import JWTUtils


def require_user_auth(request: Request) -> Optional[Tuple[str, str]]:
    # Return (username, role) if a valid JWT is found in cookies, else None
    token = request.cookies.get("access_token")
    if not token:
        return None
    user_data = JWTUtils.decode_token(token)
    if not user_data:
        return None
    return user_data["username"], user_data["role"]
