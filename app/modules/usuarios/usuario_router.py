from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.usuarios.usuario_schema import UsuarioAdminCreate, UsuarioResponse, UsuarioUpdate
from app.modules.usuarios.usuario_service import UsuarioService
from app.shared.dependencies import get_current_user, require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get(
    "",
    summary="Listar usuarios",
    description="Devuelve la lista de usuarios registrados. Requiere rol administrador.",
    response_description="Listado de usuarios.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_users(
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = UsuarioService(db).listar_usuarios()
    data = [UsuarioResponse.model_validate(user).model_dump() for user in users]
    return success_response("Lista de usuarios", data)


@router.get(
    "/{usuario_id}",
    summary="Obtener usuario por ID",
    description="Devuelve el detalle de un usuario registrado usando su identificador.",
    response_description="Detalle del usuario.",
    responses={401: {"description": "Token invalido o ausente"}, 404: {"description": "Usuario no encontrado"}},
)
def get_user(usuario_id: int, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    user = UsuarioService(db).obtener_usuario_por_id(usuario_id)
    return success_response("Detalle de usuario", UsuarioResponse.model_validate(user).model_dump())


@router.post(
    "",
    summary="Crear usuario administrativo",
    description="Crea un usuario desde el panel administrativo sin afectar la sesión del solicitante. Requiere rol administrador.",
    response_description="Usuario creado.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 409: {"description": "Correo ya registrado"}},
)
def create_user(
    payload: UsuarioAdminCreate,
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = UsuarioService(db).registrar_usuario(payload, payload.role)
    return success_response("Usuario creado", UsuarioResponse.model_validate(user).model_dump())


@router.put(
    "/{usuario_id}",
    summary="Actualizar usuario",
    description="Actualiza datos editables del usuario, como nombre, password, rol o estado activo.",
    response_description="Usuario actualizado.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 404: {"description": "Usuario no encontrado"}},
)
def update_user(
    usuario_id: int,
    payload: UsuarioUpdate,
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = UsuarioService(db).actualizar_usuario(usuario_id, payload)
    return success_response("Usuario actualizado", UsuarioResponse.model_validate(user).model_dump())


@router.delete(
    "/{usuario_id}",
    summary="Desactivar usuario",
    description="Marca un usuario como inactivo sin eliminar el registro fisicamente.",
    response_description="Usuario desactivado.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Usuario no encontrado"}},
)
def deactivate_user(
    usuario_id: int,
    _: object = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = UsuarioService(db).desactivar_usuario(usuario_id)
    return success_response("Usuario desactivado", UsuarioResponse.model_validate(user).model_dump())
