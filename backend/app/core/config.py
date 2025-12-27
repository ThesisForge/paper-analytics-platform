from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    app_name: str = "paper-analytics-platform"
    environment: str = Field("development", env="ENVIRONMENT")
    api_v1_prefix: str = "/api"
    admin_api_key: str = Field("change-me", env="ADMIN_API_KEY")

    database_url: str = Field("postgresql+psycopg2://postgres:postgres@db:5432/papers", env="DATABASE_URL")
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")

    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    arxiv_base_url: str = "https://export.arxiv.org/api/query"
    openalex_base_url: str = "https://api.openalex.org/works"

    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    metrics_enabled: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
