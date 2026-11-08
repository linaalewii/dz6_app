from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Значения по умолчанию действуют, если в .env ничего не задано."""

    app_name: str = "Учёт заказов кофейни"
    default_page_size: int = 10
    max_page_size: int = 50

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Читает настройки один раз и переиспользует."""
    return Settings()