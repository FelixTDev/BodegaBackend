from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DetalleVentaIn(BaseModel):
    producto_id: int
    quantity: float = Field(gt=0)
    unit_price: float = Field(gt=0)


class VentaCreate(BaseModel):
    number: str = Field(min_length=2, max_length=30)
    venta_type: Literal["CONTADO", "FIADO"]
    cliente_id: int | None = None
    caja_session_id: int
    subtotal: float = Field(gt=0)
    tax: float = Field(ge=0)
    total: float = Field(gt=0)
    payment_method: Literal["EFECTIVO", "TRANSFERENCIA", "YAPE", "PLIN", "TARJETA"] | None = "EFECTIVO"
    details: list[DetalleVentaIn] = Field(min_length=1)


class VentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    venta_type: str
    cliente_id: int | None
    caja_session_id: int
    usuario_id: int
    total: float
    payment_method: str | None
    status: str
