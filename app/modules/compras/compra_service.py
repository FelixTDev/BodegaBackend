from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.compras.compra_model import Compra, DetalleCompra
from app.modules.compras.compra_repository import CompraRepository


class CompraService:
    def __init__(self, db: Session):
        self.repo = CompraRepository(db)

    def create(self, payload, usuario_id: int):
        if self.repo.existe_comprobante(payload.document_number):
            raise AppException("El comprobante ya fue registrado anteriormente.", status_code=status.HTTP_409_CONFLICT)
        if not self.repo.get_proveedor(payload.proveedor_id):
            raise AppException("Proveedor no encontrado", status_code=status.HTTP_404_NOT_FOUND)

        compra = Compra(
            proveedor_id=payload.proveedor_id,
            usuario_id=usuario_id,
            document_type=payload.document_type,
            document_number=payload.document_number,
            subtotal=payload.subtotal,
            tax=payload.tax,
            total=payload.total,
            status="REGISTRADA",
        )

        try:
            self.repo.create_purchase(compra)

            for d in payload.details:
                product = self.repo.get_product(d.producto_id)
                if not product:
                    raise AppException("Producto no encontrado", status_code=status.HTTP_404_NOT_FOUND)

                self.repo.add_detail(
                    DetalleCompra(
                        compra_id=compra.id,
                        producto_id=d.producto_id,
                        quantity=d.quantity,
                        unit_cost=d.unit_cost,
                        line_subtotal=d.quantity * d.unit_cost,
                    )
                )

                product.stock_current = float(product.stock_current) + d.quantity
                self.repo.update_product(product)
                self.repo.add_inventario_movement(
                    MovimientoInventario(
                        producto_id=d.producto_id,
                        movement_type="ENTRADA",
                        reason="COMPRA",
                        quantity=d.quantity,
                        reference_type="COMPRA",
                        reference_id=compra.id,
                        usuario_id=usuario_id,
                        observacion=f"Compra {payload.document_number}",
                    )
                )

            self.repo.commit()
            self.repo.refresh(compra)
            return compra
        except Exception:
            self.repo.rollback()
            raise
