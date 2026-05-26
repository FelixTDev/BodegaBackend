from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    name: str
    description: str | None = None


class CategoriaResponse(CategoriaCreate):
    id: int

    class Config:
        from_attributes = True
