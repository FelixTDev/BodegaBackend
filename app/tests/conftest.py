from app.core.database import Base, engine
from app.main import app

# Import all models so SQLAlchemy metadata is complete during tests.
from app.modules.caja import caja_model as _caja_model
from app.modules.categorias import categoria_model as _categoria_model
from app.modules.clientes import cliente_model as _cliente_model
from app.modules.compras import compra_model as _compra_model
from app.modules.cuentas_por_cobrar import cuenta_por_cobrar_model as _cuenta_por_cobrar_model
from app.modules.inventario import inventario_model as _inventario_model
from app.modules.productos import producto_model as _producto_model
from app.modules.proveedores import proveedor_model as _proveedor_model
from app.modules.usuarios import usuario_model as _usuario_model
from app.modules.ventas import venta_model as _venta_model


Base.metadata.create_all(bind=engine, checkfirst=True)


def pytest_sessionfinish(session, exitstatus):
    Base.metadata.drop_all(bind=engine, checkfirst=True)
