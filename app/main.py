from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.database import Base, engine
from app.core.exceptions import register_exception_handlers
from app.modules.autenticacion.autenticacion_router import router as autenticacion_router
from app.modules.categorias.categoria_router import router as categoria_router
from app.modules.caja.caja_router import router as caja_router
from app.modules.clientes.cliente_router import router as cliente_router
from app.modules.inventario.inventario_router import router as inventario_router
from app.modules.productos.producto_router import router as producto_router
from app.modules.compras.compra_router import router as compra_router
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_router import router as cuenta_por_cobrar_router
from app.modules.ventas.venta_router import router as venta_router
from app.modules.proveedores.proveedor_router import router as proveedor_router
from app.modules.usuarios.usuario_router import router as usuario_router

# Ensure all models are imported so metadata includes every table before create_all
from app.modules.categorias import categoria_model as _categoria_model
from app.modules.caja import caja_model as _caja_model
from app.modules.clientes import cliente_model as _cliente_model
from app.modules.inventario import inventario_model as _inventario_model
from app.modules.productos import producto_model as _producto_model
from app.modules.compras import compra_model as _compra_model
from app.modules.cuentas_por_cobrar import cuenta_por_cobrar_model as _cuenta_por_cobrar_model
from app.modules.ventas import venta_model as _venta_model
from app.modules.proveedores import proveedor_model as _proveedor_model
from app.modules.usuarios import usuario_model as _usuario_model

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine, checkfirst=True)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(autenticacion_router, prefix=settings.api_prefix)
app.include_router(usuario_router, prefix=settings.api_prefix)
app.include_router(categoria_router, prefix=settings.api_prefix)
app.include_router(producto_router, prefix=settings.api_prefix)
app.include_router(cliente_router, prefix=settings.api_prefix)
app.include_router(proveedor_router, prefix=settings.api_prefix)
app.include_router(caja_router, prefix=settings.api_prefix)
app.include_router(compra_router, prefix=settings.api_prefix)
app.include_router(venta_router, prefix=settings.api_prefix)
app.include_router(cuenta_por_cobrar_router, prefix=settings.api_prefix)
app.include_router(inventario_router, prefix=settings.api_prefix)


@app.get("/")
def health():
    return {"success": True, "message": "Camuchita Backend running"}
