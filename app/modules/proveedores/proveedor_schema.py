from pydantic import BaseModel, ConfigDict


class ProveedorCreate(BaseModel):
    tax_id: str | None = None
    business_name: str
    contact_name: str | None = None
    phone: str | None = None
    address: str | None = None


class ProveedorResponse(ProveedorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool
