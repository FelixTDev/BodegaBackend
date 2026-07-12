from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    account_id: int
    caja_session_id: int
    document_type: Literal["RECIBO", "BOLETA"] = "RECIBO"
    document_number: str = Field(min_length=2, max_length=40)
    amount: float = Field(gt=0)
    payment_method: Literal["EFECTIVO", "TRANSFERENCIA", "YAPE", "PLIN", "TARJETA"]


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    caja_session_id: int
    usuario_id: int
    document_type: str
    document_number: str
    amount: float
    payment_method: str
    created_at: datetime | None = None


class ClienteMiniResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    names: str
    last_names: str | None = None


class CuentaPorCobrarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    venta_id: int
    cliente_id: int
    original_amount: float
    current_balance: float
    status: str
    created_at: date | None = Field(default=None, validation_alias="issue_date")
    cliente: ClienteMiniResponse | None = None
