import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}

if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.database_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Entrega una sesion SQLAlchemy por solicitud."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_database_connection() -> None:
    """Valida la conectividad inicial para detectar fallos de despliegue temprano."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("Database connection verified successfully.")
