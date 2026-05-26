from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.proveedores.proveedor_schema import ProveedorCreate, ProveedorResponse
from app.modules.proveedores.proveedor_service import ProveedorService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/suppliers", tags=["Proveedors"])


@router.post("")
def create_supplier(payload: ProveedorCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    supplier = ProveedorService(db).create(payload)
    return success_response("Proveedor created", ProveedorResponse.model_validate(supplier).model_dump())


@router.get("")
def list_suppliers(db: Session = Depends(get_db)):
    data = [ProveedorResponse.model_validate(x).model_dump() for x in ProveedorService(db).list()]
    return success_response("Proveedors list", data)
