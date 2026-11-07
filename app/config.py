from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Битрикс24
    b24_webhook_url: str = ""
    b24_application_token: str = ""

    # PostgreSQL
    database_url: str = "postgresql+asyncpg://fastapi:password@localhost:5432/fastapi_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Приложение
    app_env: str = "development"
    log_level: str = "INFO"

    # Observability
    tenant_id: str = "client_1"

settings = Settings()
