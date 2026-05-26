from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.modules.usuarios.usuario_model import Usuario
from app.modules.usuarios.usuario_repository import UsuarioRepository
from app.modules.usuarios.usuario_schema import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def registrar_usuario(self, payload: UsuarioCreate, rol: str = "user") -> Usuario:
        if rol not in {"admin", "user"}:
            raise AppException("Rol de usuario no permitido", status_code=status.HTTP_400_BAD_REQUEST)
        existente = self.repo.get_by_email(payload.email)
        if existente:
            raise AppException("Correo ya registrado", status_code=status.HTTP_409_CONFLICT)

        usuario = Usuario(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            role=rol,
            is_active=True,
        )
        return self.repo.create(usuario)

    def listar_usuarios(self) -> list[Usuario]:
        return self.repo.list_users()

    def obtener_usuario_por_id(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise AppException("Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND)
        return usuario

    def actualizar_usuario(self, usuario_id: int, payload: UsuarioUpdate) -> Usuario:
        usuario = self.obtener_usuario_por_id(usuario_id)
        if payload.full_name is not None:
            usuario.full_name = payload.full_name
        if payload.password is not None:
            usuario.hashed_password = get_password_hash(payload.password)
        if payload.role is not None:
            if payload.role not in {"admin", "user"}:
                raise AppException("Rol de usuario no permitido", status_code=status.HTTP_400_BAD_REQUEST)
            usuario.role = payload.role
        if payload.is_active is not None:
            usuario.is_active = payload.is_active
        return self.repo.update(usuario)

    def desactivar_usuario(self, usuario_id: int) -> Usuario:
        usuario = self.obtener_usuario_por_id(usuario_id)
        usuario.is_active = False
        return self.repo.update(usuario)
