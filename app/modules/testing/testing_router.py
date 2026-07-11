from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.exceptions import AppException
from app.modules.testing.testing_schema import IssueTokenRequest, IssueTokenResponse, ResetResponse
from app.modules.testing.testing_service import TestingService
from app.shared.responses import success_response

router = APIRouter(prefix="/test", tags=["Testing"])
settings = get_settings()


def require_e2e_key(x_e2e_key: str | None = Header(default=None)) -> None:
    if settings.app_env.lower() != "test":
        raise AppException("Testing routes are disabled.", status_code=status.HTTP_404_NOT_FOUND)
    if not settings.e2e_test_key or x_e2e_key != settings.e2e_test_key:
        raise AppException("Invalid E2E key.", status_code=status.HTTP_403_FORBIDDEN)


@router.post("/reset", dependencies=[Depends(require_e2e_key)])
def reset_test_data(db: Session = Depends(get_db)):
    data = TestingService(db).reset_and_seed()
    return success_response("E2E data reset", ResetResponse(**data).model_dump())


@router.post("/tokens", dependencies=[Depends(require_e2e_key)])
def issue_tokens(payload: IssueTokenRequest, db: Session = Depends(get_db)):
    data = TestingService(db).issue_tokens(
        payload.email,
        access_expired=payload.access_expired,
        refresh_expired=payload.refresh_expired,
    )
    return success_response("E2E tokens issued", IssueTokenResponse(**data).model_dump())
