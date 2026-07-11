from datetime import datetime

from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.caja.caja_repository import CajaRepository


class CajaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CajaRepository(db)

    def create_box(self, name: str):
        try:
            return self.repo.create_box(name)
        except IntegrityError as exc:
            raise AppException("Ya existe una caja con ese nombre.", status_code=status.HTTP_409_CONFLICT) from exc

    def list_boxes(self):
        return self.repo.list_boxes()

    def list_sessions(self):
        return self.repo.list_sessions()

    def open_session(self, caja_box_id: int, operation_date, opening_amount: float, usuario_id: int):
        existing = self.repo.get_open_session(caja_box_id, operation_date)
        if existing:
            raise AppException(
                "Ya existe una sesión abierta para esta caja en la fecha actual.",
                status_code=status.HTTP_409_CONFLICT,
            )
        return self.repo.create_session(
            caja_box_id=caja_box_id,
            opening_usuario_id=usuario_id,
            operation_date=operation_date,
            opening_amount=opening_amount,
            status="ABIERTA",
        )

    def close_session(self, session_id: int, closing_physical_amount: float, usuario_id: int):
        session = self.repo.get_session(session_id)
        if not session:
            raise AppException("Sesión de caja no encontrada", status_code=status.HTTP_404_NOT_FOUND)
        if session.status != "ABIERTA":
            raise AppException("Solo se puede cerrar una sesión ABIERTA.", status_code=status.HTTP_409_CONFLICT)

        try:
            in_total, out_total = self.repo.get_balance_summary(session_id)
            theoretical = float(session.opening_amount) + in_total - out_total
            difference = closing_physical_amount - theoretical
            session.closing_physical_amount = closing_physical_amount
            session.theoretical_amount = theoretical
            session.closing_difference = difference
            session.closing_usuario_id = usuario_id
            session.closed_at = datetime.utcnow()
            session.status = "CERRADA"
            saved = self.repo.update_session(session)
            return saved, theoretical, difference
        except Exception:
            self.db.rollback()
            raise
