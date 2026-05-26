import logging
from datetime import datetime
from typing import Any, Dict, Optional

# Configurar logger para auditoría
audit_logger = logging.getLogger("audit")

# Configurar handler para auditoría
if not audit_logger.handlers:
    handler = logging.FileHandler("audit.log")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.INFO)


def log_audit(
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    status: str = "SUCCESS"
) -> None:
    """
    Registra una acción de auditoría.

    Args:
        action: Tipo de acción (CREATE, UPDATE, DELETE, etc.)
        entity_type: Tipo de entidad (VENTA, COMPRA, ABONO, etc.)
        entity_id: ID de la entidad afectada
        usuario_id: ID del usuario que realizó la acción
        details: Detalles adicionales de la acción
        status: Estado de la acción (SUCCESS, FAILED, etc.)
    """
    message = f"[{status}] {action} {entity_type}"
    if entity_id:
        message += f" ID:{entity_id}"
    if usuario_id:
        message += f" USER:{usuario_id}"
    if details:
        message += f" DETAILS:{details}"

    if status == "SUCCESS":
        audit_logger.info(message)
    else:
        audit_logger.warning(message)
