from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.usuarios.usuario_schema import UsuarioResponse, UsuarioUpdate
from app.modules.usuarios.usuario_service import UsuarioService
from app.shared.dependencies import get_current_user, require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("")
def list_users(
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = UsuarioService(db).listar_usuarios()
    data = [UsuarioResponse.model_validate(user).model_dump() for user in users]
    return success_response("Lista de usuarios", data)


@router.get("/{usuario_id}")
def get_user(usuario_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UsuarioService(db).obtener_usuario_por_id(usuario_id)
    return success_response("Detalle de usuario", UsuarioResponse.model_validate(user).model_dump())


@router.put("/{usuario_id}")
def update_user(
    usuario_id: int,
    payload: UsuarioUpdate,
    _: object = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = UsuarioService(db).actualizar_usuario(usuario_id, payload)
    return success_response("Usuario actualizado", UsuarioResponse.model_validate(user).model_dump())


@router.delete("/{usuario_id}")
def deactivate_user(
    usuario_id: int,
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = UsuarioService(db).desactivar_usuario(usuario_id)
    return success_response("Usuario desactivado", UsuarioResponse.model_validate(user).model_dump())
