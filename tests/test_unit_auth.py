import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.auth.jwt_utils import JWTUtils
from app.db.models.user_model import User
from app.db.database import get_db
from app.auth.password_utils import get_password_hash, verify_password
from unittest.mock import patch


# Dummy user class used for mocking database result
class DummyUser:
    username = "test_user"
    role = "user"
    hashed_password = "hashed_pwd"


# Simulates a SQLAlchemy query with an optional user
class DummyQuery:
    def __init__(self, has_user=True):
        self.has_user = has_user

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return DummyUser() if self.has_user else None


# Simulates a SQLAlchemy session with control over user presence
class DummyDB:
    def __init__(self, has_user=True):
        self.has_user = has_user

    def query(self, model):
        return DummyQuery(has_user=self.has_user)


# Tests user extraction from a valid token and mock DB
def test_get_current_user_with_valid_token():
    token = JWTUtils.create_access_token(
        {"sub": "test_user", "role": "user"},
        expires_minutes=5
    )
    db = DummyDB(has_user=True)
    user = get_current_user(token=token, db=db)
    assert user.username == "test_user"


# Tests error raised for an invalid JWT token
def test_get_current_user_with_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid.token.here", db=DummyDB())
    assert exc_info.value.status_code == 401


# Tests error raised when token is valid but user does not exist
def test_get_current_user_with_unknown_user():
    token = JWTUtils.create_access_token(
        {"sub": "ghost", "role": "user"},
        expires_minutes=5
    )
    db = DummyDB(has_user=False)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db)
    assert exc_info.value.status_code == 401


# Tests token creation and decoding
def test_create_and_decode_token_success():
    data = {"sub": "maria", "role": "admin"}
    token = JWTUtils.create_access_token(data)
    decoded = JWTUtils.decode_token(token)
    assert decoded["username"] == "maria"
    assert decoded["role"] == "admin"


# Tests decoding an invalid token returns None
def test_decode_invalid_token_returns_none():
    result = JWTUtils.decode_token("invalid.token.payload")
    assert result is None


# Tests password hashing returns a different value than input
def test_get_password_hash_returns_different_value():
    raw_password = "secure123"
    hashed = get_password_hash(raw_password)
    assert isinstance(hashed, str)
    assert hashed != raw_password


# Tests password verification with matching raw and hashed passwords
def test_verify_password_matches_correctly():
    raw_password = "my_secret"
    hashed = get_password_hash(raw_password)
    assert verify_password(raw_password, hashed)


# Tests password verification fails on wrong input
def test_verify_password_fails_on_incorrect_input():
    hashed = get_password_hash("real_password")
    assert not verify_password("wrong_password", hashed)
