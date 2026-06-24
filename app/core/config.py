from __future__ import annotations

from pydantic import AliasChoices, Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(
        default="Checkpoint", validation_alias=AliasChoices("APP_NAME", "app_name")
    )
    debug: bool = Field(default=False, validation_alias=AliasChoices("APP_DEBUG", "app_debug"))
    host: str = Field(default="127.0.0.1", validation_alias=AliasChoices("APP_HOST", "app_host"))
    port: int = Field(default=8000, validation_alias=AliasChoices("APP_PORT", "app_port"))
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5436/checkpoint",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    token_secret_key: str = Field(
        default="change-me",
        validation_alias=AliasChoices("TOKEN_SECRET_KEY", "token_secret_key"),
    )
    token_issuer: str = Field(
        default="checkpoint",
        validation_alias=AliasChoices("TOKEN_ISSUER", "token_issuer"),
    )
    access_token_lifetime_minutes: PositiveInt = Field(
        default=60,
        validation_alias=AliasChoices(
            "ACCESS_TOKEN_LIFETIME_MINUTES",
            "access_token_lifetime_minutes",
        ),
    )


settings = Settings()
