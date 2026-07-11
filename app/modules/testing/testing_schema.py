from pydantic import BaseModel, Field


class ResetResponse(BaseModel):
    admin_email: str
    admin_password: str
    user_email: str
    user_password: str
    product_ids: dict[str, int]
    client_id: int
    supplier_id: int
    box_id: int


class IssueTokenRequest(BaseModel):
    email: str
    access_expired: bool = False
    refresh_expired: bool = False


class IssueTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
