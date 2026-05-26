from pydantic import BaseModel, ConfigDict, Field


class ProductoCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    barcode: str | None = Field(default=None, max_length=80)
    name: str = Field(min_length=1, max_length=140)
    categoria_id: int | None = None
    brand: str | None = Field(default=None, max_length=80)
    unit_measure: str = Field(default="UND", min_length=1, max_length=20)
    venta_price: float = Field(gt=0)
    unit_cost: float | None = Field(default=None, gt=0)
    stock_current: float = Field(ge=0)
    stock_minimum: float = Field(ge=0)


class AjusteInventarioRequest(BaseModel):
    cantidad: float = Field(gt=0)
    motivo: str = Field(min_length=3, max_length=30)


class ProductoResponse(ProductoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool
