from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app

client = TestClient(app)
TEST_EMAIL = f"test_{uuid4().hex[:10]}@example.com"
TEST_PASSWORD = "password123"


def test_register_user():
    payload = {
        "email": TEST_EMAIL,
        "full_name": "Test Usuario 1",
        "password": TEST_PASSWORD,
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]


def test_login_success():
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_login_invalid_password():
    payload = {"email": TEST_EMAIL, "password": "wrongpass123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_protected_route_with_token():
    login = client.post("/api/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    token = login.json()["data"]["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_protected_route_without_token():
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_protected_route_with_invalid_token_returns_401():
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert "token" in body["message"].lower()
