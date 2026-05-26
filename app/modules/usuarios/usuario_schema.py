from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=140)


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=128)


class UsuarioUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=140)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: Literal["admin", "user"] | None = None
    is_active: bool | None = None


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
