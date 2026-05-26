from pydantic import BaseModel


class ProveedorCreate(BaseModel):
    tax_id: str | None = None
    business_name: str
    contact_name: str | None = None
    phone: str | None = None
    address: str | None = None


class ProveedorResponse(ProveedorCreate):
    id: int
    active: bool

    class Config:
        from_attributes = True
