from pydantic import BaseModel, ConfigDict, Field


class DetalleCompraIn(BaseModel):
    producto_id: int
    quantity: float = Field(gt=0)
    unit_cost: float = Field(gt=0)


class CompraCreate(BaseModel):
    proveedor_id: int
    document_type: str = Field(min_length=3, max_length=20)
    document_number: str = Field(min_length=2, max_length=40)
    subtotal: float = Field(gt=0)
    tax: float = Field(ge=0)
    total: float = Field(gt=0)
    details: list[DetalleCompraIn] = Field(min_length=1)


class CompraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    proveedor_id: int
    usuario_id: int
    document_type: str
    document_number: str
    subtotal: float
    tax: float
    total: float
    status: str
