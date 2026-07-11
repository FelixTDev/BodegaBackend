from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.caja.caja_model import MovimientoCaja
from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_model import CuentaPorCobrar
from app.modules.ventas.venta_model import Venta, DetalleVenta
from app.modules.ventas.venta_repository import VentaRepository


class VentaService:
    def __init__(self, db: Session):
        self.repo = VentaRepository(db)

    def create(self, payload, usuario_id: int):
        if self.repo.existe_numero_venta(payload.number):
            raise AppException("El número de venta ya existe.", status_code=status.HTTP_409_CONFLICT)

        session = self.repo.get_caja_session(payload.caja_session_id)
        if not session or session.status != "ABIERTA":
            raise AppException("Debe existir una caja abierta para registrar la venta.", status_code=status.HTTP_409_CONFLICT)

        if payload.venta_type == "CONTADO" and payload.cliente_id is not None:
            raise AppException("La venta CONTADO no debe asociar cliente.", status_code=status.HTTP_400_BAD_REQUEST)
        if payload.venta_type == "FIADO" and payload.cliente_id is None:
            raise AppException("La venta FIADO requiere cliente.", status_code=status.HTTP_400_BAD_REQUEST)

        client = None
        if payload.cliente_id:
            client = self.repo.get_client(payload.cliente_id)
            if not client:
                raise AppException("Cliente no encontrado", status_code=status.HTTP_404_NOT_FOUND)

        if payload.venta_type == "FIADO":
            if client.credit_status in {"MOROSO", "BLOQUEADO"}:
                raise AppException("El cliente se encuentra bloqueado para ventas al fiado.", status_code=status.HTTP_409_CONFLICT)
            if float(client.pending_balance) + payload.total > float(client.credit_limit):
                raise AppException("El fiado excede el límite de crédito disponible.", status_code=status.HTTP_409_CONFLICT)

        venta = Venta(
            number=payload.number,
            venta_type=payload.venta_type,
            cliente_id=payload.cliente_id,
            caja_session_id=payload.caja_session_id,
            usuario_id=usuario_id,
            subtotal=payload.subtotal,
            tax=payload.tax,
            total=payload.total,
            payment_method=payload.payment_method if payload.venta_type == "CONTADO" else None,
            status="EMITIDA",
        )

        try:
            self.repo.add_sale(venta)

            for d in payload.details:
                product = self.repo.get_product(d.producto_id)
                if not product:
                    raise AppException("Producto no encontrado", status_code=status.HTTP_404_NOT_FOUND)
                if float(product.stock_current) < d.quantity:
                    raise AppException("No hay stock suficiente para realizar la venta.", status_code=status.HTTP_409_CONFLICT)

                self.repo.add_venta_detail(
                    DetalleVenta(
                        venta_id=venta.id,
                        producto_id=d.producto_id,
                        quantity=d.quantity,
                        unit_price=d.unit_price,
                        unit_tax=0,
                        line_subtotal=d.quantity * d.unit_price,
                    )
                )
                product.stock_current = float(product.stock_current) - d.quantity
                self.repo.update_product(product)
                self.repo.add_inventario_movement(
                    MovimientoInventario(
                        producto_id=d.producto_id,
                        movement_type="SALIDA",
                        reason="VENTA",
                        quantity=d.quantity,
                        reference_type="VENTA",
                        reference_id=venta.id,
                        usuario_id=usuario_id,
                        observacion=f"Venta {payload.number}",
                    )
                )

            if payload.venta_type == "FIADO":
                self.repo.add_receivable(
                    CuentaPorCobrar(
                        venta_id=venta.id,
                        cliente_id=payload.cliente_id,
                        original_amount=payload.total,
                        current_balance=payload.total,
                        status="PENDIENTE",
                    )
                )
                client.pending_balance = float(client.pending_balance) + payload.total
                self.repo.update_client(client)

            if payload.venta_type == "CONTADO":
                self.repo.add_caja_movement(
                    MovimientoCaja(
                        caja_session_id=payload.caja_session_id,
                        movement_type="INGRESO",
                        source="VENTA_CONTADO",
                        reference_type="VENTA",
                        reference_id=venta.id,
                        amount=payload.total,
                        payment_method=payload.payment_method,
                    )
                )

            self.repo.commit()
            self.repo.refresh(venta)
            return venta
        except Exception:
            self.repo.rollback()
            raise

    def list(self):
        return self.repo.list_sales()
