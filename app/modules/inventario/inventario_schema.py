from pydantic import BaseModel


class MovimientoInventarioResponse(BaseModel):
    id: int
    producto_id: int
    movement_type: str
    reason: str
    quantity: float
    reference_type: str | None = None
    reference_id: int | None = None

    class Config:
        from_attributes = True
