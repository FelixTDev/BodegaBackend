from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.caja.caja_model import MovimientoCaja, SesionCaja
from app.modules.clientes.cliente_model import Cliente
from app.modules.inventario.inventario_model import MovimientoInventario
from app.modules.productos.producto_model import Producto
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_model import CuentaPorCobrar
from app.modules.ventas.venta_model import Venta, DetalleVenta


class VentaRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_numero_venta(self, numero: str) -> bool:
        stmt = select(Venta).where(Venta.number == numero)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def get_caja_session(self, caja_session_id: int):
        return self.db.get(SesionCaja, caja_session_id)

    def get_product(self, producto_id: int):
        return self.db.get(Producto, producto_id)

    def get_client(self, cliente_id: int):
        return self.db.get(Cliente, cliente_id)

    def add_sale(self, sale: Venta):
        self.db.add(sale)
        self.db.flush()
        return sale

    def add_venta_detail(self, detail: DetalleVenta):
        self.db.add(detail)

    def update_product(self, product: Producto):
        self.db.add(product)

    def update_client(self, client: Cliente):
        self.db.add(client)

    def add_inventario_movement(self, movement: MovimientoInventario):
        self.db.add(movement)

    def add_receivable(self, receivable: CuentaPorCobrar):
        self.db.add(receivable)

    def add_caja_movement(self, movement: MovimientoCaja):
        self.db.add(movement)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, obj):
        self.db.refresh(obj)
