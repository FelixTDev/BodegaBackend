from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductoMiniResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str | None = None


class UsuarioMiniResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    role: str


class MovimientoInventarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    movement_type: str
    reason: str
    quantity: float
    reference_type: str | None = None
    reference_id: int | None = None
    usuario_id: int | None = None
    observacion: str | None = None
    created_at: datetime | None = None
    producto: ProductoMiniResponse | None = None
    usuario: UsuarioMiniResponse | None = None
