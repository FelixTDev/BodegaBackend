from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_schema import CuentaPorCobrarResponse, PaymentCreate, PaymentResponse
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_service import CuentaPorCobrarService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/receivables", tags=["Cuentas por Cobrar"])


@router.get(
    "",
    summary="Listar cuentas por cobrar",
    description="Devuelve las cuentas por cobrar registradas y su saldo actual. Requiere rol administrador.",
    response_description="Listado de cuentas por cobrar.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_receivables(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    receivables = CuentaPorCobrarService(db).list_accounts()
    data = [CuentaPorCobrarResponse.model_validate(account).model_dump() for account in receivables]
    return success_response("Lista de cuentas por cobrar", data)


@router.get(
    "/payments",
    summary="Listar abonos",
    description="Devuelve el historial de abonos registrados sobre cuentas por cobrar. Requiere rol administrador.",
    response_description="Listado de abonos.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_payments(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    payments = CuentaPorCobrarService(db).list_payments()
    data = [PaymentResponse.model_validate(payment).model_dump() for payment in payments]
    return success_response("Lista de abonos", data)


@router.post(
    "/payments",
    summary="Registrar abono",
    description="Registra un abono sobre una cuenta por cobrar y actualiza los saldos relacionados. Requiere rol administrador.",
    response_description="Abono registrado.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Cuenta por cobrar no encontrada"}, 409: {"description": "Conflicto de negocio"}},
)
def register_payment(payload: PaymentCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    payment = CuentaPorCobrarService(db).registrar_abono(payload, user.id)
    return success_response("Abono registrado", PaymentResponse.model_validate(payment).model_dump())
