from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.db.repositories.user_repository import get_user_by_username
from app.db.database import get_db
from app.utils.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Extracts the current user from the JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # Predefined exception for failed authentication
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # Extract username from the token payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        # Raise exception if token is invalid or tampered
        raise credentials_exception

    # Fetch the user from the database by username
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    # Return the user object if everything is valid
    return user
