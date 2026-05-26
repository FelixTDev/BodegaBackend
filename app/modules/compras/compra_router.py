from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.compras.compra_schema import CompraCreate, CompraResponse
from app.modules.compras.compra_service import CompraService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/purchases", tags=["Compras"])


@router.post("")
def create_purchase(payload: CompraCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    purchase = CompraService(db).create(payload, user.id)
    return success_response("Compra created", CompraResponse.model_validate(purchase).model_dump())
