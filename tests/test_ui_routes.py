import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app


# Mocks publish_log, Redis cache, and require_user_auth for all UI route tests
@pytest.fixture
def client_with_patch():
    with patch("app.controllers.math_controller.publish_log"), \
         patch("app.middleware.error_logging.publish_log"), \
         patch("app.services.math_service.get_cached_result", return_value=None), \
         patch("app.services.math_service.set_cached_result"), \
         patch("app.auth.ui_auth_guard.require_user_auth") as mock_guard:
        client = TestClient(app)
        yield client, mock_guard


# Tests if login/register form is shown
def test_show_login_page(client_with_patch):
    client, _ = client_with_patch
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower() or "register" in response.text.lower()


# Tests successful registration (200 + success message)
def test_register_success(client_with_patch):
    client, _ = client_with_patch
    with patch("httpx.AsyncClient.post", return_value=MagicMock(status_code=200, json=lambda: {})):
        response = client.post("/register", data={"username": "test", "password": "pass"})
    assert response.status_code == 200
    assert "user registered successfully" in response.text.lower()


# Tests failed registration due to duplicate username
def test_register_fail(client_with_patch):
    client, _ = client_with_patch
    with patch("httpx.AsyncClient.post", return_value=MagicMock(status_code=400)):
        response = client.post("/register", data={"username": "test", "password": "pass"})
    assert response.status_code == 200
    assert "username already taken" in response.text.lower()


# Tests login form sends request and sets the access_token cookie
def test_login_success_sets_cookie(client_with_patch):
    client, _ = client_with_patch
    token = "fake.jwt.token"
    mock_response = MagicMock(status_code=200, json=lambda: {"access_token": token})
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        response = client.post(
            "/login",
            data={"username": "test_user", "password": "secret"},
            follow_redirects=False
        )
    assert response.status_code == 302
    assert response.headers["location"] == "/math"
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] == token


# Tests that logout removes the access_token cookie and redirects
def test_logout_deletes_cookie(client_with_patch):
    client, _ = client_with_patch
    client.cookies.set("access_token", "some_token")
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"
    assert "access_token" not in response.cookies or response.cookies["access_token"] == ""


# Tests redirect to /login when accessing /math without authentication
def test_math_page_requires_login(client_with_patch):
    client, mock_guard = client_with_patch
    mock_guard.return_value = None
    response = client.get("/math", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("/login")


# Tests redirect to /login when accessing /logs without authentication
def test_logs_requires_auth(client_with_patch):
    client, mock_guard = client_with_patch
    mock_guard.return_value = None
    response = client.get("/logs", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("/login")
