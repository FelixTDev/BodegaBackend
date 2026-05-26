from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.productos.producto_schema import AjusteInventarioRequest, ProductoCreate, ProductoResponse
from app.modules.productos.producto_service import ProductoService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/products", tags=["Productos"])


@router.post("")
def create_product(payload: ProductoCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    product = ProductoService(db).create(payload)
    return success_response("Producto creado", ProductoResponse.model_validate(product).model_dump())


@router.get("")
def list_products(db: Session = Depends(get_db)):
    data = [ProductoResponse.model_validate(x).model_dump() for x in ProductoService(db).list()]
    return success_response("Lista de productos", data)


@router.post("/{producto_id}/ajustes")
def ajustar_stock_manual(
    producto_id: int,
    payload: AjusteInventarioRequest,
    usuario = Depends(require_admin),
    db: Session = Depends(get_db),
):
    producto = ProductoService(db).registrar_ajuste_manual(producto_id, payload.cantidad, payload.motivo, usuario.id)
    return success_response("Ajuste de inventario registrado", ProductoResponse.model_validate(producto).model_dump())
