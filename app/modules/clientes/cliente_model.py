from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    document: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    names: Mapped[str] = mapped_column(String(120), nullable=False)
    last_names: Mapped[str | None] = mapped_column(String(120), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    address: Mapped[str | None] = mapped_column(String(180), nullable=True)
    credit_limit: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    pending_balance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    credit_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVO")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
