from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.caja.caja_model import Caja, MovimientoCaja, SesionCaja


class CajaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_box(self, name: str):
        box = Caja(name=name, active=True)
        self.db.add(box)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(box)
        return box

    def list_boxes(self):
        stmt = select(Caja).order_by(Caja.id.desc())
        return self.db.execute(stmt).scalars().all()

    def list_sessions(self):
        stmt = select(SesionCaja).order_by(SesionCaja.id.desc())
        return self.db.execute(stmt).scalars().all()

    def get_open_session(self, caja_box_id: int, operation_date):
        stmt = select(SesionCaja).where(
            SesionCaja.caja_box_id == caja_box_id,
            SesionCaja.operation_date == operation_date,
            SesionCaja.status == "ABIERTA",
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_session(self, **kwargs):
        session = SesionCaja(**kwargs)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: int):
        return self.db.get(SesionCaja, session_id)

    def update_session(self, session: SesionCaja):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def add_movement(self, **kwargs):
        movement = MovimientoCaja(**kwargs)
        self.db.add(movement)

    def get_balance_summary(self, session_id: int):
        incomes = self.db.execute(
            select(MovimientoCaja).where(MovimientoCaja.caja_session_id == session_id, MovimientoCaja.movement_type == "INGRESO")
        ).scalars().all()
        expenses = self.db.execute(
            select(MovimientoCaja).where(MovimientoCaja.caja_session_id == session_id, MovimientoCaja.movement_type == "EGRESO")
        ).scalars().all()
        in_total = sum(float(x.amount) for x in incomes)
        out_total = sum(float(x.amount) for x in expenses)
        return in_total, out_total
