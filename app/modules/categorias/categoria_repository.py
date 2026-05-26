from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.categorias.categoria_model import Categoria
from app.modules.categorias.categoria_schema import CategoriaCreate


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CategoriaCreate) -> Categoria:
        obj = Categoria(name=data.name, description=data.description)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self) -> list[Categoria]:
        return list(self.db.execute(select(Categoria).order_by(Categoria.id)).scalars().all())
