from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.productos.producto_model import Producto
from app.modules.proveedores.proveedor_model import Proveedor
from app.modules.compras.compra_model import Compra, DetalleCompra


class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_comprobante(self, numero: str) -> bool:
        stmt = select(Compra).where(Compra.document_number == numero)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def list_purchases(self):
        stmt = select(Compra).order_by(Compra.id.desc())
        return self.db.execute(stmt).scalars().all()

    def get_proveedor(self, proveedor_id: int):
        return self.db.get(Proveedor, proveedor_id)

    def create_purchase(self, purchase: Compra):
        self.db.add(purchase)
        self.db.flush()
        return purchase

    def add_detail(self, detail: DetalleCompra):
        self.db.add(detail)

    def get_product(self, producto_id: int):
        return self.db.get(Producto, producto_id)

    def update_product(self, product: Producto):
        self.db.add(product)

    def add_inventario_movement(self, movement: MovimientoInventario):
        self.db.add(movement)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, obj):
        self.db.refresh(obj)
