from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.compras.compra_schema import CompraCreate, CompraResponse
from app.modules.compras.compra_service import CompraService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/purchases", tags=["Compras"])


@router.get(
    "",
    summary="Listar compras",
    description="Devuelve el historial de compras registradas. Requiere rol administrador.",
    response_description="Listado de compras.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def list_purchases(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    purchases = CompraService(db).list()
    data = [CompraResponse.model_validate(purchase).model_dump() for purchase in purchases]
    return success_response("Lista de compras", data)


@router.post(
    "",
    summary="Registrar compra",
    description="Crea una compra y actualiza el inventario asociado a sus detalles. Requiere rol administrador.",
    response_description="Compra registrada.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Proveedor o producto no encontrado"}, 409: {"description": "Conflicto de negocio"}},
)
def create_purchase(payload: CompraCreate, user=Depends(require_admin), db: Session = Depends(get_db)):
    purchase = CompraService(db).create(payload, user.id)
    return success_response("Compra created", CompraResponse.model_validate(purchase).model_dump())
