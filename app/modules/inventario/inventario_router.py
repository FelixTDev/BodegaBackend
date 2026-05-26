from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.inventario.inventario_schema import MovimientoInventarioResponse
from app.modules.inventario.inventario_service import InventarioService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/inventory", tags=["Inventario"])


@router.get("/movements")
def list_movements(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    data = [MovimientoInventarioResponse.model_validate(x).model_dump() for x in InventarioService(db).list()]
    return success_response("Inventario movements list", data)
