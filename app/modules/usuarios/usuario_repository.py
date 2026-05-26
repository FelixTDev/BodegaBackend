from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.usuarios.usuario_model import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        return self.db.get(Usuario, usuario_id)

    def get_by_email(self, email: str) -> Usuario | None:
        stmt = select(Usuario).where(Usuario.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_users(self) -> list[Usuario]:
        stmt = select(Usuario).order_by(Usuario.id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, user: Usuario) -> Usuario:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: Usuario) -> Usuario:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def guardar(self, user: Usuario) -> Usuario:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
