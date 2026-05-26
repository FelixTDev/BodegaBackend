from sqlalchemy.orm import Session

from app.modules.inventario.inventario_repository import InventarioRepository


class InventarioService:
    def __init__(self, db: Session):
        self.repo = InventarioRepository(db)

    def list(self):
        return self.repo.list()
