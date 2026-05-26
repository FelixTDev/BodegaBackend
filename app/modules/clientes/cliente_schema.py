from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteCreate(BaseModel):
    document: str | None = Field(default=None, max_length=20)
    names: str = Field(min_length=2, max_length=120)
    last_names: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=180)
    credit_limit: float = Field(ge=0)


class ClienteResponse(ClienteCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pending_balance: float
    credit_status: Literal["ACTIVO", "MOROSO", "BLOQUEADO"]
