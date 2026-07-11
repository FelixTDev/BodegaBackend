from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.productos.producto_schema import AjusteInventarioRequest, ProductoCreate, ProductoResponse
from app.modules.productos.producto_service import ProductoService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/products", tags=["Productos"])


@router.post(
    "",
    summary="Crear producto",
    description="Registra un producto nuevo dentro del catalogo. Requiere rol administrador.",
    response_description="Producto creado.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 409: {"description": "Conflicto de negocio"}},
)
def create_product(payload: ProductoCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    product = ProductoService(db).create(payload)
    return success_response("Producto creado", ProductoResponse.model_validate(product).model_dump())


@router.get(
    "",
    summary="Listar productos",
    description="Devuelve el catalogo actual de productos registrados.",
    response_description="Listado de productos.",
)
def list_products(db: Session = Depends(get_db)):
    data = [ProductoResponse.model_validate(x).model_dump() for x in ProductoService(db).list()]
    return success_response("Lista de productos", data)


@router.post(
    "/{producto_id}/ajustes",
    summary="Ajustar stock manualmente",
    description="Registra un ajuste manual de inventario para un producto especifico. Requiere rol administrador.",
    response_description="Producto actualizado tras el ajuste.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}, 404: {"description": "Producto no encontrado"}},
)
def ajustar_stock_manual(
    producto_id: int,
    payload: AjusteInventarioRequest,
    usuario=Depends(require_admin),
    db: Session = Depends(get_db),
):
    producto = ProductoService(db).registrar_ajuste_manual(producto_id, payload.cantidad, payload.motivo, usuario.id)
    return success_response("Ajuste de inventario registrado", ProductoResponse.model_validate(producto).model_dump())
