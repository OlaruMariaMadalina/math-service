import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.main import app
from app.db.database import get_db
from app.db.models.user_model import User
from app.utils.config import settings
from jose import jwt


client = TestClient(app)


# Automatically mocks Redis logging in all tests
@pytest.fixture(autouse=True)
def mock_publish_log():
    with patch("app.controllers.math_controller.publish_log") as mock_log_controller, \
         patch("app.middleware.error_logging.publish_log") as mock_log_middleware:
        yield mock_log_controller


# Deletes the test user before and after each test
@pytest.fixture
def clear_test_user():
    db: Session = next(get_db())
    user = db.query(User).filter_by(username="test_user").first()
    if user:
        db.delete(user)
        db.commit()
    yield
    user = db.query(User).filter_by(username="test_user").first()
    if user:
        db.delete(user)
        db.commit()


# Tests successful registration with new username
def test_register_user_success(clear_test_user):
    payload = {
        "username": "test_user",
        "password": "test123",
        "role": "user"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    assert "registered with role" in response.json()["msg"]


# Tests error on duplicate registration attempt
def test_register_user_duplicate(clear_test_user):
    payload = {
        "username": "test_user",
        "password": "test123",
        "role": "user"
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


# Tests login with correct username and password
def test_login_success(clear_test_user):
    register_payload = {
        "username": "test_user",
        "password": "test123",
        "role": "user"
    }
    client.post("/auth/register", json=register_payload)

    login_payload = {
        "username": "test_user",
        "password": "test123"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    decoded = jwt.decode(
        data["access_token"],
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    assert decoded["sub"] == "test_user"
    assert decoded["role"] == "user"


# Tests login failure due to incorrect password
def test_login_wrong_password(clear_test_user):
    payload = {
        "username": "test_user",
        "password": "test123",
        "role": "user"
    }
    client.post("/auth/register", json=payload)

    login_payload = {
        "username": "test_user",
        "password": "wrong_password"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


# Tests login failure with non-existent user
def test_login_nonexistent_user():
    login_payload = {
        "username": "ghost_user",
        "password": "doesnt_matter"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 401
