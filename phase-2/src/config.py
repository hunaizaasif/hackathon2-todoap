"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database
    database_url: str

    # Authentication
    auth_secret_key: str = "76lYYDv3HxxlE19Gf3u5SMN8Las00JcM"
    # auth_api_url: str = "https://auth.example.com"  # Future use

    # Application
    app_name: str = "Phase 2 Todo API"
    debug: bool = False
    cors_origins: List[str] = ["*"]

    # Server
    host: str = "0.0.0.0"
    port: int = 8001


# Global settings instance
settings = Settings()
