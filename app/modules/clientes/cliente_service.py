from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.clientes.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def create(self, payload):
        if payload.credit_limit < 0:
            raise AppException("Límite de crédito inválido", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if self.repo.existe_duplicado(payload.document, payload.phone, payload.email):
            raise AppException("Ya existe un cliente con el mismo documento, teléfono o correo", status_code=status.HTTP_409_CONFLICT)
        return self.repo.create(payload)

    def list(self):
        return self.repo.list()

    def get(self, cliente_id: int):
        cliente = self.repo.get(cliente_id)
        if not cliente:
            raise AppException("Cliente no encontrado", status_code=status.HTTP_404_NOT_FOUND)
        return cliente
