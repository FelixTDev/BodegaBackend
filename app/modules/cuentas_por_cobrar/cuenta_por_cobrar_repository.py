from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.caja.caja_model import MovimientoCaja, SesionCaja
from app.modules.clientes.cliente_model import Cliente
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_model import Abono, CuentaPorCobrar


class CuentaPorCobrarRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_comprobante_abono(self, numero: str) -> bool:
        stmt = select(Abono).where(Abono.document_number == numero)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def list_accounts(self):
        stmt = select(CuentaPorCobrar).order_by(CuentaPorCobrar.id.desc())
        return self.db.execute(stmt).scalars().all()

    def list_payments(self):
        stmt = select(Abono).order_by(Abono.id.desc())
        return self.db.execute(stmt).scalars().all()

    def get_account(self, account_id: int):
        return self.db.get(CuentaPorCobrar, account_id)

    def get_session(self, session_id: int):
        return self.db.get(SesionCaja, session_id)

    def get_client(self, cliente_id: int):
        return self.db.get(Cliente, cliente_id)

    def add_payment(self, payment: Abono):
        self.db.add(payment)
        self.db.flush()
        return payment

    def update_account(self, account: CuentaPorCobrar):
        self.db.add(account)

    def update_client(self, client: Cliente):
        self.db.add(client)

    def add_caja_movement(self, movement: MovimientoCaja):
        self.db.add(movement)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, obj):
        self.db.refresh(obj)
