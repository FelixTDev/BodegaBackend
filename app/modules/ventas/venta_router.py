from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.ventas.venta_schema import VentaCreate, VentaResponse
from app.modules.ventas.venta_service import VentaService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/sales", tags=["Ventas"])


@router.post("")
def create_sale(payload: VentaCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    sale = VentaService(db).create(payload, user.id)
    return success_response("Venta created", VentaResponse.model_validate(sale).model_dump())
