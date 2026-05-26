from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.proveedores.proveedor_model import Proveedor


class ProveedorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload):
        obj = Proveedor(**payload.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, proveedor_id: int):
        return self.db.get(Proveedor, proveedor_id)

    def list(self):
        return list(self.db.execute(select(Proveedor).order_by(Proveedor.id)).scalars().all())
