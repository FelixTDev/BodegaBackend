from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.categorias.categoria_schema import CategoriaCreate, CategoriaResponse
from app.modules.categorias.categoria_service import CategoriaService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.post(
    "",
    summary="Crear categoria",
    description="Crea una categoria para organizar productos. Requiere rol administrador.",
    response_description="Categoria creada.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Token invalido o ausente"}, 403: {"description": "Permisos insuficientes"}},
)
def create_category(payload: CategoriaCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    obj = CategoriaService(db).create(payload)
    return success_response("Categoria created", CategoriaResponse.model_validate(obj).model_dump())


@router.get(
    "",
    summary="Listar categorias",
    description="Devuelve la lista de categorias registradas.",
    response_description="Listado de categorias.",
)
def list_categories(db: Session = Depends(get_db)):
    data = [CategoriaResponse.model_validate(x).model_dump() for x in CategoriaService(db).list()]
    return success_response("Categories list", data)
