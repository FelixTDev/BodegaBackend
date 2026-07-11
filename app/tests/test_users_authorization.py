from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.modules.usuarios.usuario_service import UsuarioService
from app.modules.usuarios.usuario_schema import UsuarioCreate

client = TestClient(app)


def _create_user(role: str) -> tuple[str, str]:
    unique = uuid4().hex[:10]
    email = f"{role}_{unique}@example.com"
    password = "password123"
    db = SessionLocal()
    try:
      UsuarioService(db).registrar_usuario(
          UsuarioCreate(email=email, full_name=f"{role} user", password=password),
          role,
      )
    finally:
      db.close()
    return email, password


def _login_headers(email: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_users_endpoints_require_authentication():
    assert client.get("/api/users").status_code == 401
    assert client.post("/api/users", json={}).status_code == 401
    assert client.put("/api/users/1", json={"full_name": "X"}).status_code == 401
    assert client.delete("/api/users/1").status_code == 401


def test_regular_user_cannot_access_admin_user_endpoints():
    email, password = _create_user("user")
    headers = _login_headers(email, password)

    assert client.get("/api/users", headers=headers).status_code == 403
    assert client.post(
        "/api/users",
        headers=headers,
        json={"email": f"new_{uuid4().hex[:6]}@example.com", "full_name": "Nuevo", "password": "password123", "role": "user"},
    ).status_code == 403
    assert client.get("/api/users/1", headers=headers).status_code == 403
    assert client.put("/api/users/1", headers=headers, json={"full_name": "Cambio"}).status_code == 403
    assert client.delete("/api/users/1", headers=headers).status_code == 403


def test_admin_can_manage_users():
    email, password = _create_user("admin")
    headers = _login_headers(email, password)

    list_response = client.get("/api/users", headers=headers)
    assert list_response.status_code == 200

    create_response = client.post(
        "/api/users",
        headers=headers,
        json={"email": f"managed_{uuid4().hex[:6]}@example.com", "full_name": "Managed User", "password": "password123", "role": "user"},
    )
    assert create_response.status_code == 200

    created_id = create_response.json()["data"]["id"]
    assert client.get(f"/api/users/{created_id}", headers=headers).status_code == 200
    assert client.put(f"/api/users/{created_id}", headers=headers, json={"role": "admin"}).status_code == 200
    assert client.delete(f"/api/users/{created_id}", headers=headers).status_code == 200
