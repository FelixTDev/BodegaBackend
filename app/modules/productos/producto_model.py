from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Producto(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False, index=True)
    categoria_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
    brand: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    unit_measure: Mapped[str] = mapped_column(String(20), nullable=False, default="UND")
    venta_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    stock_current: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    stock_minimum: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
