from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.categorias.categoria_schema import CategoriaCreate, CategoriaResponse
from app.modules.categorias.categoria_service import CategoriaService
from app.shared.dependencies import require_admin
from app.shared.responses import success_response

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("")
def create_category(payload: CategoriaCreate, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    obj = CategoriaService(db).create(payload)
    return success_response("Categoria created", CategoriaResponse.model_validate(obj).model_dump())


@router.get("")
def list_categories(db: Session = Depends(get_db)):
    data = [CategoriaResponse.model_validate(x).model_dump() for x in CategoriaService(db).list()]
    return success_response("Categories list", data)
