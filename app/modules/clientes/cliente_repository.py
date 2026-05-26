from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.modules.clientes.cliente_model import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_duplicado(self, document: str | None, phone: str | None, email: str | None):
        filtros = []
        if document:
            filtros.append(Cliente.document == document)
        if phone:
            filtros.append(Cliente.phone == phone)
        if email:
            filtros.append(Cliente.email == email)
        if not filtros:
            return False
        stmt = select(Cliente).where(or_(*filtros))
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def create(self, payload):
        obj = Cliente(**payload.model_dump(), pending_balance=0, credit_status="ACTIVO")
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self):
        return list(self.db.execute(select(Cliente).order_by(Cliente.id)).scalars().all())

    def get(self, cliente_id: int):
        return self.db.get(Cliente, cliente_id)

    def update(self, obj: Cliente):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
