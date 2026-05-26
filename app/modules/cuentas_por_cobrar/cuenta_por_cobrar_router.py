from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_schema import PaymentCreate, PaymentResponse
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_service import CuentaPorCobrarService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/receivables", tags=["CuentaPorCobrars"])


@router.post("/payments")
def register_payment(payload: PaymentCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    payment = CuentaPorCobrarService(db).registrar_abono(payload, user.id)
    return success_response("Abono registrado", PaymentResponse.model_validate(payment).model_dump())
