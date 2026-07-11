from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.main import app
from app.core.database import SessionLocal
from app.modules.usuarios.usuario_model import Usuario


client = TestClient(app)


def _create_admin_user() -> tuple[str, str]:
    unique = uuid4().hex[:8]
    email = f"admin_{unique}@example.com"
    password = "12345678"
    db = SessionLocal()
    try:
        user = Usuario(
            email=email,
            full_name=f"Admin {unique}",
            hashed_password=get_password_hash(password),
            role="admin",
            is_active=True,
        )
        db.add(user)
        db.commit()
        return email, password
    finally:
        db.close()


def _get_admin_headers() -> dict[str, str]:
    email, password = _create_admin_user()
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_missing_listing_endpoints_return_real_data():
    headers = _get_admin_headers()
    unique = uuid4().hex[:6]

    category_response = client.post(
        "/api/categories",
        json={"name": f"Bebidas {unique}", "description": "Categoria para pruebas"},
        headers=headers,
    )
    assert category_response.status_code == 200
    categoria_id = category_response.json()["data"]["id"]

    supplier_response = client.post(
        "/api/suppliers",
        json={
            "tax_id": f"SUP-{unique}",
            "business_name": f"Proveedor {unique}",
            "contact_name": "Contacto QA",
            "phone": "999999999",
            "address": "Direccion QA",
        },
        headers=headers,
    )
    assert supplier_response.status_code == 200
    proveedor_id = supplier_response.json()["data"]["id"]

    product_response = client.post(
        "/api/products",
        json={
            "code": f"PRD-{unique}",
            "barcode": f"BAR-{unique}",
            "name": f"Producto {unique}",
            "categoria_id": categoria_id,
            "brand": "Marca QA",
            "unit_measure": "UND",
            "venta_price": 15,
            "unit_cost": 10,
            "stock_current": 0,
            "stock_minimum": 1,
            "active": True,
        },
        headers=headers,
    )
    assert product_response.status_code == 200
    producto_id = product_response.json()["data"]["id"]

    box_response = client.post("/api/cash/boxes", json={"name": f"Caja {unique}"}, headers=headers)
    assert box_response.status_code == 200
    caja_box_id = box_response.json()["data"]["id"]

    open_session_response = client.post(
        "/api/cash/sessions/open",
        json={
            "caja_box_id": caja_box_id,
            "operation_date": str(date.today()),
            "opening_amount": 100,
        },
        headers=headers,
    )
    assert open_session_response.status_code == 200
    caja_session_id = open_session_response.json()["data"]["id"]

    client_response = client.post(
        "/api/clients",
        json={
            "document": f"DOC-{unique}",
            "names": "Cliente",
            "last_names": "QA",
            "phone": f"98{unique}",
            "email": f"cliente_{unique}@example.com",
            "address": "Direccion cliente",
            "credit_limit": 500,
        },
        headers=headers,
    )
    assert client_response.status_code == 200
    cliente_id = client_response.json()["data"]["id"]

    purchase_response = client.post(
        "/api/purchases",
        json={
            "proveedor_id": proveedor_id,
            "document_type": "FACTURA",
            "document_number": f"FAC-{unique}",
            "subtotal": 100,
            "tax": 0,
            "total": 100,
            "details": [{"producto_id": producto_id, "quantity": 10, "unit_cost": 10}],
        },
        headers=headers,
    )
    assert purchase_response.status_code == 200

    sale_response = client.post(
        "/api/sales",
        json={
            "number": f"VTA-{unique}",
            "venta_type": "FIADO",
            "cliente_id": cliente_id,
            "caja_session_id": caja_session_id,
            "subtotal": 30,
            "tax": 0,
            "total": 30,
            "payment_method": "EFECTIVO",
            "details": [{"producto_id": producto_id, "quantity": 2, "unit_price": 15}],
        },
        headers=headers,
    )
    assert sale_response.status_code == 200
    venta_id = sale_response.json()["data"]["id"]

    receivables_list = client.get("/api/receivables", headers=headers)
    assert receivables_list.status_code == 200
    receivable = next(item for item in receivables_list.json()["data"] if item["venta_id"] == venta_id)

    payment_response = client.post(
        "/api/receivables/payments",
        json={
            "account_id": receivable["id"],
            "caja_session_id": caja_session_id,
            "document_type": "RECIBO",
            "document_number": f"RCP-{unique}",
            "amount": 10,
            "payment_method": "EFECTIVO",
        },
        headers=headers,
    )
    assert payment_response.status_code == 200
    payment_id = payment_response.json()["data"]["id"]

    boxes_list = client.get("/api/cash/boxes", headers=headers)
    assert boxes_list.status_code == 200
    assert any(item["id"] == caja_box_id for item in boxes_list.json()["data"])

    sessions_list = client.get("/api/cash/sessions", headers=headers)
    assert sessions_list.status_code == 200
    assert any(item["id"] == caja_session_id for item in sessions_list.json()["data"])

    purchases_list = client.get("/api/purchases", headers=headers)
    assert purchases_list.status_code == 200
    assert any(item["document_number"] == f"FAC-{unique}" for item in purchases_list.json()["data"])

    sales_list = client.get("/api/sales", headers=headers)
    assert sales_list.status_code == 200
    assert any(item["number"] == f"VTA-{unique}" for item in sales_list.json()["data"])

    receivables_list_after_payment = client.get("/api/receivables", headers=headers)
    assert receivables_list_after_payment.status_code == 200
    updated = next(item for item in receivables_list_after_payment.json()["data"] if item["venta_id"] == venta_id)
    assert updated["current_balance"] == 20

    payments_list = client.get("/api/receivables/payments", headers=headers)
    assert payments_list.status_code == 200
    assert any(item["id"] == payment_id for item in payments_list.json()["data"])
