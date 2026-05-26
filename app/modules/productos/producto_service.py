from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.productos.producto_repository import ProductoRepository


class ProductoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductoRepository(db)

    def create(self, payload):
        if self.repo.existe_por_codigo(payload.code):
            raise AppException("Ya existe un producto con ese código", status_code=status.HTTP_409_CONFLICT)
        return self.repo.create(payload)

    def list(self):
        return self.repo.list()

    def update_stock(self, producto_id: int, delta: float):
        product = self.repo.get(producto_id)
        if not product:
            raise AppException("Producto no encontrado", status_code=status.HTTP_404_NOT_FOUND)
        if float(product.stock_current) + delta < 0:
            raise AppException("No hay stock suficiente para realizar la operación.", status_code=status.HTTP_409_CONFLICT)
        product.stock_current = float(product.stock_current) + delta
        return self.repo.update(product)

    def registrar_ajuste_manual(self, producto_id: int, cantidad: float, motivo: str, usuario_id: int):
        product = self.repo.get(producto_id)
        if not product:
            raise AppException("Producto no encontrado", status_code=status.HTTP_404_NOT_FOUND)
        if not motivo.strip():
            raise AppException("El motivo del ajuste es obligatorio", status_code=status.HTTP_400_BAD_REQUEST)
        if float(product.stock_current) + cantidad < 0:
            raise AppException("No hay stock suficiente para realizar el ajuste.", status_code=status.HTTP_409_CONFLICT)

        try:
            product.stock_current = float(product.stock_current) + cantidad
            self.db.add(product)
            self.db.add(
                MovimientoInventario(
                    producto_id=producto_id,
                    movement_type="AJUSTE",
                    reason=motivo.strip().upper(),
                    quantity=abs(cantidad),
                    reference_type="AJUSTE",
                    reference_id=producto_id,
                    usuario_id=usuario_id,
                    observacion=motivo.strip(),
                )
            )
            self.db.commit()
            self.db.refresh(product)
            return product
        except Exception:
            self.db.rollback()
            raise
