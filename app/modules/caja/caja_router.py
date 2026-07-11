from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.caja.caja_schema import (
    CajaCreate,
    CajaResponse,
    SesionCajaResponse,
    CloseSesionCajaRequest,
    OpenSesionCajaRequest,
)
from app.modules.caja.caja_service import CajaService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/cash", tags=["Caja"])


@router.get(
    "/boxes",
    summary="Listar cajas",
    description="Devuelve las cajas fisicas registradas en el sistema. Requiere rol administrador.",
    response_description="Listado de cajas.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_caja_boxes(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    boxes = CajaService(db).list_boxes()
    data = [CajaResponse.model_validate(box).model_dump() for box in boxes]
    return success_response("Lista de cajas", data)


@router.post(
    "/boxes",
    summary="Crear caja",
    description="Registra una nueva caja operativa del sistema. Requiere rol administrador.",
    response_description="Caja creada.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def create_caja_box(payload: CajaCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    box = CajaService(db).create_box(payload.name)
    return success_response("Caja creada", CajaResponse.model_validate(box).model_dump())


@router.get(
    "/sessions",
    summary="Listar sesiones de caja",
    description="Devuelve el historial de sesiones de caja registradas. Requiere rol administrador.",
    response_description="Listado de sesiones de caja.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_sessions(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    sessions = CajaService(db).list_sessions()
    data = [SesionCajaResponse.model_validate(session).model_dump() for session in sessions]
    return success_response("Lista de sesiones de caja", data)


@router.post(
    "/sessions/open",
    summary="Abrir sesion de caja",
    description="Abre una sesion diaria de caja con monto inicial. Requiere rol administrador.",
    response_description="Sesion de caja abierta.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 409: {"description": "La caja ya tiene una sesion abierta"}},
)
def open_session(payload: OpenSesionCajaRequest, user=Depends(require_admin), db: Session = Depends(get_db)):
    session = CajaService(db).open_session(payload.caja_box_id, payload.operation_date, payload.opening_amount, user.id)
    return success_response("Sesión de caja abierta", SesionCajaResponse.model_validate(session).model_dump())


@router.post(
    "/sessions/{session_id}/close",
    summary="Cerrar sesion de caja",
    description="Cierra la sesion de caja y devuelve monto teorico y diferencia contra el monto fisico. Requiere rol administrador.",
    response_description="Sesion de caja cerrada.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Sesion no encontrada"}, 409: {"description": "Conflicto de negocio"}},
)
def close_session(session_id: int, payload: CloseSesionCajaRequest, user=Depends(require_admin), db: Session = Depends(get_db)):
    session, theoretical, diff = CajaService(db).close_session(session_id, payload.closing_physical_amount, user.id)
    return success_response(
        "Sesión de caja cerrada",
        {
            "session": SesionCajaResponse.model_validate(session).model_dump(),
            "theoretical_amount": theoretical,
            "difference": diff,
        },
    )
