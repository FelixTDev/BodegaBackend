from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CajaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)


class CajaResponse(CajaCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool


class OpenSesionCajaRequest(BaseModel):
    caja_box_id: int
    operation_date: date
    opening_amount: float = Field(ge=0)


class CloseSesionCajaRequest(BaseModel):
    closing_physical_amount: float = Field(ge=0)


class SesionCajaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    caja_box_id: int
    opening_usuario_id: int
    closing_usuario_id: int | None = None
    operation_date: date
    opening_amount: float
    closing_physical_amount: float | None = None
    theoretical_amount: float | None = None
    closing_difference: float | None = None
    status: str
    opened_at: datetime | None = None
