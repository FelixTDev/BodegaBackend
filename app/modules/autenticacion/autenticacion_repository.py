from sqlalchemy.orm import Session

from app.modules.usuarios.usuario_model import Usuario
from app.modules.usuarios.usuario_repository import UsuarioRepository


class AutenticacionRepository:
    def __init__(self, db: Session):
        self.users = UsuarioRepository(db)

    def get_usuario_by_email(self, email: str) -> Usuario | None:
        return self.users.get_by_email(email)

    def get_usuario_by_id(self, usuario_id: int) -> Usuario | None:
        return self.users.get_by_id(usuario_id)
