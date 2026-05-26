from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import decode_token
from app.modules.usuarios.usuario_model import Usuario
from app.modules.usuarios.usuario_repository import UsuarioRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise AppException("Token de acceso inválido.", status_code=status.HTTP_401_UNAUTHORIZED)

    subject = payload.get("sub")
    if not subject:
        raise AppException("Token de acceso inválido.", status_code=status.HTTP_401_UNAUTHORIZED)

    user = UsuarioRepository(db).get_by_id(int(subject))
    if not user:
        raise AppException("Usuario no encontrado", status_code=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        raise AppException("El usuario está inactivo.", status_code=status.HTTP_403_FORBIDDEN)
    return user


def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.role.lower() != "admin":
        raise AppException("Solo un usuario ADMIN puede realizar esta operación.", status_code=status.HTTP_403_FORBIDDEN)
    return current_user
