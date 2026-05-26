from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.autenticacion.autenticacion_schema import LoginRequest, RefreshRequest, RegisterRequest, TokenPairResponse
from app.modules.autenticacion.autenticacion_service import AutenticacionService
from app.modules.usuarios.usuario_schema import UsuarioResponse
from app.shared.dependencies import get_current_user
from app.shared.responses import success_response

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).registrar_usuario(payload)
    return success_response("Usuario registrado", TokenPairResponse(**tokens).model_dump())


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).iniciar_sesion(payload)
    return success_response("Inicio de sesión exitoso", TokenPairResponse(**tokens).model_dump())


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).refrescar_token(payload)
    return success_response("Token refrescado", TokenPairResponse(**tokens).model_dump())


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return success_response("Current user", UsuarioResponse.model_validate(current_user).model_dump())
