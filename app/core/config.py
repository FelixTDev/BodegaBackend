from functools import lru_cache
from typing import Any

from pydantic import Field, computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centraliza la configuracion del backend para local y produccion."""

    app_name: str = "Camuchita Backend"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    api_prefix: str = "/api"

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    db_host: str | None = None
    db_port: int = 3306
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None

    secret_key: str = Field(...)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    frontend_url: str | None = None
    allowed_cors_origins_raw: str = Field(default="", alias="ALLOWED_CORS_ORIGINS")
    backend_url: str | None = None
    port: int = 8000
    e2e_test_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def build_database_url(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        if data.get("DATABASE_URL") or data.get("database_url"):
            return data

        db_host = data.get("DB_HOST") or data.get("db_host")
        db_name = data.get("DB_NAME") or data.get("db_name")
        db_user = data.get("DB_USER") or data.get("db_user")
        db_password = data.get("DB_PASSWORD") or data.get("db_password", "")
        db_port = data.get("DB_PORT") or data.get("db_port") or 3306

        if db_host and db_name and db_user:
            data["DATABASE_URL"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return data

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str | None) -> str:
        if not value or not value.strip():
            raise ValueError("DATABASE_URL o las variables DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD son obligatorias")
        return value

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("SECRET_KEY es obligatorio")
        return value

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        insecure_secret = "change-this-secret-key"
        if self.app_env.lower() != "development" and self.secret_key == insecure_secret:
            raise ValueError("SECRET_KEY debe cambiarse antes de desplegar en entornos no locales")
        return self

    @computed_field(return_type=list[str])
    @property
    def allowed_cors_origins(self) -> list[str]:
        origins: list[str] = []
        if self.frontend_url:
            origins.append(self.frontend_url.rstrip("/"))

        extra_origins = [
            origin.strip().rstrip("/")
            for origin in self.allowed_cors_origins_raw.split(",")
            if origin.strip()
        ]
        for origin in extra_origins:
            if origin not in origins:
                origins.append(origin)
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()
