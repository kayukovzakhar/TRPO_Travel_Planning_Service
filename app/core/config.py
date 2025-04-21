import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyHttpUrl, field_validator
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = "Travel Planner API"
    API_V1_STR: str = "/api/v1"

    # Security Settings
    SECRET_KEY: str = "your-super-secret-key-please-change"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/travel_planner"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "travel_planner_db"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> str:
        return str(PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=int(self.POSTGRES_PORT),
            path=f"/{self.POSTGRES_DB}",
        ))

    # Add other settings like CORS origins if needed
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"

# Instantiate settings
settings = Settings()

# --- Remove Temporary Hardcoded Settings --- 
# DATABASE_URL = "postgresql://postgres:password@localhost/travel_planner_db"

# Example usage:
# from .config import settings
# db_url = settings.DATABASE_URL 