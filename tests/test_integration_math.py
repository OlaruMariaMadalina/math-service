import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from jose import jwt
from unittest.mock import patch

from app.main import app
from app.db.database import get_db
from app.db.models.user_model import User
from app.utils.config import settings


# Mocks Redis logging and caching for all tests
@pytest.fixture
def mock_publish_log_and_cache():
    with patch("app.controllers.math_controller.publish_log") as mock_log_controller, \
         patch("app.middleware.error_logging.publish_log") as mock_log_middleware, \
         patch("app.services.math_service.get_cached_result", return_value=None) as mock_cache_get, \
         patch("app.services.math_service.set_cached_result") as mock_cache_set:
        yield


# Provides a test client with mocks applied
@pytest.fixture
def client(mock_publish_log_and_cache):
    return TestClient(app)


# Creates and cleans up a test user in the database
@pytest.fixture
def test_user():
    db: Session = next(get_db())
    user = User(
        username="test_user",
        hashed_password="not_used_here",
        role="user"
    )
    db.add(user)
    db.commit()
    db.flush()
    yield user
    db.delete(user)
    db.commit()
    db.flush()


# Generates an Authorization header with a valid JWT for the test user
@pytest.fixture
def auth_header(test_user):
    token = jwt.encode(
        {"sub": test_user.username, "role": test_user.role},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {token}"}


# Tests the /fibonacci endpoint with a valid input
def test_fibonacci(auth_header, test_user, client):
    payload = {"n": 7}
    response = client.post("/fibonacci", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "fib"
    assert data["result"] == 13
    assert data["input"] == {"n": 7}
    assert data["user"] == test_user.username


# Tests the /power endpoint with base and exponent values
def test_power(auth_header, test_user, client):
    payload = {"base": 2, "exponent": 3}
    response = client.post("/power", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "pow"
    assert data["result"] == 8
    assert data["input"] == {"base": 2, "exponent": 3}
    assert data["user"] == test_user.username


# Tests the /factorial endpoint with a valid input
def test_factorial(auth_header, test_user, client):
    payload = {"n": 5}
    response = client.post("/factorial", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "factorial"
    assert data["result"] == 120
    assert data["input"] == {"n": 5}
    assert data["user"] == test_user.username
