from sqlalchemy.orm import Session

from app.modules.categorias.categoria_repository import CategoriaRepository
from app.modules.categorias.categoria_schema import CategoriaCreate


class CategoriaService:
    def __init__(self, db: Session):
        self.repo = CategoriaRepository(db)

    def create(self, payload: CategoriaCreate):
        return self.repo.create(payload)

    def list(self):
        return self.repo.list()
