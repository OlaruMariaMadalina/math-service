from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.user_repository import (
    get_user_by_username,
    create_user,
)
from app.auth.password_utils import (
    get_password_hash,
    verify_password,
)
from app.auth.jwt_utils import JWTUtils
from app.schemas.user_schemas import RegisterRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Check if username is already taken
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the user's password before storing it
    hashed_password = get_password_hash(data.password)

    # Save the new user in the database
    user = create_user(db, data.username, hashed_password, data.role)
    return {
        "msg": (
            f"User '{user.username}' registered with role '{user.role}'"
        )
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Retrieve user by username
    user = get_user_by_username(db, form_data.username)

    # Validate credentials
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )

    # Generate JWT access token with role and 30min expiry
    token = JWTUtils.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_minutes=30
    )
    return {"access_token": token, "token_type": "bearer"}
