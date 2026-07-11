from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from fastapi import status
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.core.security import _create_token, get_password_hash
from app.modules.caja.caja_model import Caja, SesionCaja
from app.modules.categorias.categoria_model import Categoria
from app.modules.clientes.cliente_model import Cliente
from app.modules.compras.compra_model import Compra, DetalleCompra
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_model import CuentaPorCobrar
from app.modules.productos.producto_model import Producto
from app.modules.proveedores.proveedor_model import Proveedor
from app.modules.usuarios.usuario_model import Usuario
from app.modules.ventas.venta_model import DetalleVenta, Venta


ADMIN_EMAIL = "admin.e2e@example.com"
ADMIN_PASSWORD = "AdminE2E!123"
USER_EMAIL = "user.e2e@example.com"
USER_PASSWORD = "UserE2E!123"


class TestingService:
    def __init__(self, db: Session):
        self.db = db

    def reset_and_seed(self) -> dict[str, object]:
        self.db.close()
        Base.metadata.drop_all(bind=engine, checkfirst=True)
        Base.metadata.create_all(bind=engine, checkfirst=True)

        admin = Usuario(
            email=ADMIN_EMAIL,
            full_name="Admin E2E",
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
        user = Usuario(
            email=USER_EMAIL,
            full_name="User E2E",
            hashed_password=get_password_hash(USER_PASSWORD),
            role="user",
            is_active=True,
        )
        self.db.add_all([admin, user])
        self.db.flush()

        category = Categoria(name="Bebidas", description="Categoria base E2E")
        self.db.add(category)
        self.db.flush()

        product_a = Producto(
            code="E2E-INKA-01",
            barcode="775999100001",
            name="Inka Cola 500ml",
            categoria_id=category.id,
            brand="Inka Cola",
            unit_measure="UND",
            venta_price=5.00,
            unit_cost=3.20,
            stock_current=20,
            stock_minimum=2,
            active=True,
        )
        product_b = Producto(
            code="E2E-AGUA-01",
            barcode="775999100002",
            name="Agua 625ml",
            categoria_id=category.id,
            brand="San Luis",
            unit_measure="UND",
            venta_price=2.50,
            unit_cost=1.40,
            stock_current=30,
            stock_minimum=4,
            active=True,
        )
        self.db.add_all([product_a, product_b])
        self.db.flush()

        supplier = Proveedor(
            tax_id="20123456789",
            business_name="Proveedor E2E SAC",
            contact_name="Logistica E2E",
            phone="999111222",
            address="Av. Prueba 123",
            active=True,
        )
        client = Cliente(
            document="44556677",
            names="Cliente E2E",
            last_names="Perez",
            phone="988777666",
            email="cliente.e2e@example.com",
            address="Jr. Cliente 456",
            credit_limit=200.00,
            pending_balance=80.00,
            credit_status="ACTIVO",
        )
        self.db.add_all([supplier, client])
        self.db.flush()

        box = Caja(name="Caja Principal E2E", active=True)
        self.db.add(box)
        self.db.flush()

        closed_session = SesionCaja(
            caja_box_id=box.id,
            opening_usuario_id=admin.id,
            closing_usuario_id=admin.id,
            operation_date=date.today() - timedelta(days=1),
            opening_amount=100.00,
            closing_physical_amount=180.00,
            theoretical_amount=180.00,
            closing_difference=0.00,
            status="CERRADA",
            closed_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        self.db.add(closed_session)
        self.db.flush()

        sale = Venta(
            number="E2E-FIADO-001",
            venta_type="FIADO",
            cliente_id=client.id,
            caja_session_id=closed_session.id,
            usuario_id=admin.id,
            subtotal=67.80,
            tax=12.20,
            total=80.00,
            payment_method=None,
            status="EMITIDA",
        )
        self.db.add(sale)
        self.db.flush()

        self.db.add(
            DetalleVenta(
                venta_id=sale.id,
                producto_id=product_a.id,
                quantity=2,
                unit_price=5.00,
                unit_tax=0,
                line_subtotal=10.00,
            )
        )
        self.db.add(
            CuentaPorCobrar(
                venta_id=sale.id,
                cliente_id=client.id,
                original_amount=80.00,
                current_balance=80.00,
                issue_date=date.today() - timedelta(days=1),
                due_date=date.today() + timedelta(days=7),
                status="PENDIENTE",
            )
        )

        historical_purchase = Compra(
            proveedor_id=supplier.id,
            usuario_id=admin.id,
            document_type="FACTURA",
            document_number="E2E-HIST-001",
            subtotal=32.00,
            tax=5.76,
            total=37.76,
            status="REGISTRADA",
        )
        self.db.add(historical_purchase)
        self.db.flush()
        self.db.add(
            DetalleCompra(
                compra_id=historical_purchase.id,
                producto_id=product_b.id,
                quantity=5,
                unit_cost=1.40,
                line_subtotal=7.00,
            )
        )

        self.db.commit()

        return {
            "admin_email": ADMIN_EMAIL,
            "admin_password": ADMIN_PASSWORD,
            "user_email": USER_EMAIL,
            "user_password": USER_PASSWORD,
            "product_ids": {
                "inka_cola": product_a.id,
                "agua": product_b.id,
            },
            "client_id": client.id,
            "supplier_id": supplier.id,
            "box_id": box.id,
        }

    def issue_tokens(self, email: str, *, access_expired: bool, refresh_expired: bool) -> dict[str, str]:
        user = self.db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise AppException("Usuario E2E no encontrado.", status_code=status.HTTP_404_NOT_FOUND)

        access_delta = timedelta(minutes=-1) if access_expired else timedelta(minutes=30)
        refresh_delta = timedelta(minutes=-1) if refresh_expired else timedelta(days=7)

        return {
            "access_token": _create_token(str(user.id), access_delta, "access", {"role": user.role}),
            "refresh_token": _create_token(str(user.id), refresh_delta, "refresh"),
            "token_type": "bearer",
        }
