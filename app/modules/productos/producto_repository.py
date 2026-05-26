from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.productos.producto_model import Producto


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_por_codigo(self, code: str):
        stmt = select(Producto).where(Producto.code == code)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def tiene_movimientos(self, producto_id: int) -> bool:
        stmt = select(MovimientoInventario).where(MovimientoInventario.producto_id == producto_id)
        return self.db.execute(stmt).first() is not None

    def create(self, payload):
        obj = Producto(**payload.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self):
        return list(self.db.execute(select(Producto).order_by(Producto.id)).scalars().all())

    def get(self, producto_id: int):
        return self.db.get(Producto, producto_id)

    def update(self, obj: Producto):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
