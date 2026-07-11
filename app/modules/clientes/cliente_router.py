from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.clientes.cliente_schema import ClienteCreate, ClienteResponse
from app.modules.clientes.cliente_service import ClienteService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/clients", tags=["Clientes"])


@router.post(
    "",
    summary="Crear cliente",
    description="Registra un cliente nuevo en el sistema. Requiere rol administrador.",
    response_description="Cliente creado.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def create_client(payload: ClienteCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    client = ClienteService(db).create(payload)
    return success_response("Cliente created", ClienteResponse.model_validate(client).model_dump())


@router.get(
    "",
    summary="Listar clientes",
    description="Devuelve la lista de clientes registrados.",
    response_description="Listado de clientes.",
)
def list_clients(db: Session = Depends(get_db)):
    data = [ClienteResponse.model_validate(x).model_dump() for x in ClienteService(db).list()]
    return success_response("Clientes list", data)
