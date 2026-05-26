from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Caja(Base):
    __tablename__ = "caja_boxes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)


class SesionCaja(Base):
    __tablename__ = "caja_sessions"
    __table_args__ = (UniqueConstraint("caja_box_id", "operation_date", "status", name="uq_caja_session_status"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    caja_box_id: Mapped[int] = mapped_column(ForeignKey("caja_boxes.id"), nullable=False)
    opening_usuario_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    closing_usuario_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    operation_date: Mapped[date] = mapped_column(Date, nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    opening_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    closing_physical_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    theoretical_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    closing_difference: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="ABIERTA")


class MovimientoCaja(Base):
    __tablename__ = "caja_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    caja_session_id: Mapped[int] = mapped_column(ForeignKey("caja_sessions.id"), nullable=False)
    movement_type: Mapped[str] = mapped_column(String(15), nullable=False)
    source: Mapped[str] = mapped_column(String(25), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    reference_id: Mapped[int | None] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
