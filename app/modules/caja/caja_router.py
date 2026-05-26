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


@router.post("/boxes")
def create_caja_box(payload: CajaCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    box = CajaService(db).create_box(payload.name)
    return success_response("Caja creada", CajaResponse.model_validate(box).model_dump())


@router.post("/sessions/open")
def open_session(payload: OpenSesionCajaRequest, user=Depends(require_admin), db: Session = Depends(get_db)):
    session = CajaService(db).open_session(payload.caja_box_id, payload.operation_date, payload.opening_amount, user.id)
    return success_response("Sesión de caja abierta", SesionCajaResponse.model_validate(session).model_dump())


@router.post("/sessions/{session_id}/close")
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
