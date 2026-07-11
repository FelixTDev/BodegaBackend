from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.autenticacion.autenticacion_schema import LoginRequest, RefreshRequest, RegisterRequest, TokenPairResponse
from app.modules.autenticacion.autenticacion_service import AutenticacionService
from app.modules.usuarios.usuario_schema import UsuarioResponse
from app.shared.dependencies import get_current_user
from app.shared.responses import success_response

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/register",
    summary="Registrar usuario",
    description="Crea un usuario y devuelve el par de tokens inicial para autenticar futuras solicitudes.",
    response_description="Registro exitoso con access token y refresh token.",
    responses={400: {"description": "Datos invalidos"}, 409: {"description": "Correo ya registrado"}, 500: {"description": "Error interno"}},
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).registrar_usuario(payload)
    return success_response("Usuario registrado", TokenPairResponse(**tokens).model_dump())


@router.post(
    "/login",
    summary="Iniciar sesion",
    description="Autentica un usuario existente y devuelve tokens JWT para acceder al resto de endpoints protegidos.",
    response_description="Inicio de sesion exitoso.",
    responses={400: {"description": "Datos invalidos"}, 401: {"description": "Credenciales invalidas"}, 403: {"description": "Usuario inactivo"}},
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).iniciar_sesion(payload)
    return success_response("Inicio de sesión exitoso", TokenPairResponse(**tokens).model_dump())


@router.post(
    "/refresh",
    summary="Refrescar token",
    description="Genera un nuevo access token a partir de un refresh token valido.",
    response_description="Token refrescado correctamente.",
    responses={400: {"description": "Payload invalido"}, 401: {"description": "Refresh token invalido o expirado"}},
)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    tokens = AutenticacionService(db).refrescar_token(payload)
    return success_response("Token refrescado", TokenPairResponse(**tokens).model_dump())


@router.get(
    "/me",
    summary="Obtener usuario autenticado",
    description="Devuelve los datos del usuario asociado al access token enviado en la cabecera Authorization.",
    response_description="Datos del usuario autenticado.",
    responses={401: {"description": "Token invalido o ausente"}, 403: {"description": "Usuario inactivo"}},
)
def me(current_user=Depends(get_current_user)):
    return success_response("Current user", UsuarioResponse.model_validate(current_user).model_dump())
