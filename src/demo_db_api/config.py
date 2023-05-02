from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""
    DB_URL: str = "sqlite:///data/app.db"


@lru_cache()
def get_settings():
    return Settings()