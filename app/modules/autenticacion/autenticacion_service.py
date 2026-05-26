from datetime import datetime, timezone

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.modules.autenticacion.autenticacion_repository import AutenticacionRepository
from app.modules.autenticacion.autenticacion_schema import LoginRequest, RefreshRequest, RegisterRequest
from app.modules.usuarios.usuario_schema import UsuarioCreate
from app.modules.usuarios.usuario_service import UsuarioService


class AutenticacionService:
    def __init__(self, db: Session):
        self.repo = AutenticacionRepository(db)
        self.usuario_service = UsuarioService(db)

    def registrar_usuario(self, payload: RegisterRequest):
        user = self.usuario_service.registrar_usuario(
            UsuarioCreate(email=payload.email, full_name=payload.full_name, password=payload.password)
        )
        return self._construir_tokens(str(user.id), user.role)

    def iniciar_sesion(self, payload: LoginRequest):
        user = self.repo.get_usuario_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise AppException("Credenciales inválidas", status_code=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            raise AppException("Usuario inactivo", status_code=status.HTTP_403_FORBIDDEN)
        user.last_login_at = datetime.now(timezone.utc)
        self.repo.users.guardar(user)
        return self._construir_tokens(str(user.id), user.role)

    def refrescar_token(self, payload: RefreshRequest):
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise AppException("Refresh token inválido", status_code=status.HTTP_401_UNAUTHORIZED)

        usuario_id = token_data.get("sub")
        if not usuario_id:
            raise AppException("Refresh token inválido", status_code=status.HTTP_401_UNAUTHORIZED)

        user = self.repo.get_usuario_by_id(int(usuario_id))
        if not user or not user.is_active:
            raise AppException("Usuario inactivo o inexistente", status_code=status.HTTP_401_UNAUTHORIZED)

        return self._construir_tokens(str(user.id), user.role)

    @staticmethod
    def _construir_tokens(usuario_id: str, role: str) -> dict[str, str]:
        return {
            "access_token": create_access_token(usuario_id, role),
            "refresh_token": create_refresh_token(usuario_id),
            "token_type": "bearer",
        }
