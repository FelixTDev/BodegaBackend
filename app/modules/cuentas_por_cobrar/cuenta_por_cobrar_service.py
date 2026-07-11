from datetime import date

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.caja.caja_model import MovimientoCaja
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_model import Abono
from app.modules.cuentas_por_cobrar.cuenta_por_cobrar_repository import CuentaPorCobrarRepository


class CuentaPorCobrarService:
    def __init__(self, db: Session):
        self.repo = CuentaPorCobrarRepository(db)

    def registrar_abono(self, payload, usuario_id: int):
        if self.repo.existe_comprobante_abono(payload.document_number):
            raise AppException("El comprobante ya fue registrado anteriormente.", status_code=status.HTTP_409_CONFLICT)

        session = self.repo.get_session(payload.caja_session_id)
        if not session or session.status != "ABIERTA":
            raise AppException("Debe existir una caja abierta para registrar el abono.", status_code=status.HTTP_409_CONFLICT)

        account = self.repo.get_account(payload.account_id)
        if not account:
            raise AppException("Cuenta por cobrar no encontrada", status_code=status.HTTP_404_NOT_FOUND)
        if account.status == "CANCELADA":
            raise AppException("La cuenta por cobrar ya está cancelada.", status_code=status.HTTP_409_CONFLICT)
        if payload.amount > float(account.current_balance):
            raise AppException("El monto del abono no puede ser mayor al saldo pendiente.", status_code=status.HTTP_409_CONFLICT)

        client = self.repo.get_client(account.cliente_id)
        if not client:
            raise AppException("Cliente no encontrado", status_code=status.HTTP_404_NOT_FOUND)

        try:
            abono = Abono(
                account_id=payload.account_id,
                caja_session_id=payload.caja_session_id,
                usuario_id=usuario_id,
                document_type=payload.document_type,
                document_number=payload.document_number,
                amount=payload.amount,
                payment_method=payload.payment_method,
            )
            self.repo.add_payment(abono)

            new_balance = float(account.current_balance) - payload.amount
            account.current_balance = new_balance
            if new_balance == 0:
                account.status = "CANCELADA"
            elif account.due_date and account.due_date < date.today():
                account.status = "VENCIDA"
            else:
                account.status = "PENDIENTE"

            client.pending_balance = max(0, float(client.pending_balance) - payload.amount)

            self.repo.update_account(account)
            self.repo.update_client(client)
            self.repo.add_caja_movement(
                MovimientoCaja(
                    caja_session_id=payload.caja_session_id,
                    movement_type="INGRESO",
                    source="ABONO",
                    reference_type="ABONO",
                    reference_id=abono.id,
                    amount=payload.amount,
                    payment_method=payload.payment_method,
                )
            )
            self.repo.commit()
            self.repo.refresh(abono)
            return abono
        except Exception:
            self.repo.rollback()
            raise

    def list_accounts(self):
        return self.repo.list_accounts()

    def list_payments(self):
        return self.repo.list_payments()
