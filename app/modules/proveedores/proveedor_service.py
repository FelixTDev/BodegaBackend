from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.proveedores.proveedor_repository import ProveedorRepository


class ProveedorService:
    def __init__(self, db: Session):
        self.repo = ProveedorRepository(db)

    def create(self, payload):
        return self.repo.create(payload)

    def get(self, proveedor_id: int):
        supplier = self.repo.get(proveedor_id)
        if not supplier:
            raise AppException("Proveedor not found", status_code=status.HTTP_404_NOT_FOUND)
        return supplier

    def list(self):
        return self.repo.list()
