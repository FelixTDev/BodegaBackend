from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Camuchita Backend"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    api_prefix: str = "/api"

    database_url: str = Field(..., alias="DATABASE_URL")

    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("database_url")
    @classmethod
    def validar_database_url(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("DATABASE_URL es obligatorio en el archivo .env")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
