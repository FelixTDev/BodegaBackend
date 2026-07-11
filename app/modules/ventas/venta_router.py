from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.ventas.venta_schema import VentaCreate, VentaResponse
from app.modules.ventas.venta_service import VentaService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/sales", tags=["Ventas"])


@router.get(
    "",
    summary="Listar ventas",
    description="Devuelve el historial de ventas registradas. Requiere rol administrador.",
    response_description="Listado de ventas.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_sales(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    sales = VentaService(db).list()
    data = [VentaResponse.model_validate(sale).model_dump() for sale in sales]
    return success_response("Lista de ventas", data)


@router.post(
    "",
    summary="Registrar venta",
    description="Crea una venta, valida reglas de negocio y descuenta stock cuando corresponde. Requiere rol administrador.",
    response_description="Venta registrada.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Cliente o producto no encontrado"}, 409: {"description": "Conflicto de negocio"}},
)
def create_sale(payload: VentaCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    sale = VentaService(db).create(payload, user.id)
    return success_response("Venta created", VentaResponse.model_validate(sale).model_dump())
