from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.inventario.inventario_model import MovimientoInventario


class InventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_movement(self, **kwargs):
        obj = MovimientoInventario(**kwargs)
        self.db.add(obj)
        return obj

    def list(self):
        return list(self.db.execute(select(MovimientoInventario).order_by(MovimientoInventario.id.desc())).scalars().all())
