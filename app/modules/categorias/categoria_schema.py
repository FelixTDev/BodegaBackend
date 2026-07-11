from pydantic import BaseModel, ConfigDict


class CategoriaCreate(BaseModel):
    name: str
    description: str | None = None


class CategoriaResponse(CategoriaCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
