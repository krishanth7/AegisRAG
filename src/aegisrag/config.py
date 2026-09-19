"""Typed runtime configuration."""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AEGISRAG_", extra="ignore")
    collection: str = "private-reports"
    chroma_path: Path = Path("./chroma_db")
    upload_path: Path = Path("./uploads")
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"
    top_k: int = Field(default=5, ge=1, le=20)
    max_upload_mb: int = Field(default=25, ge=1, le=200)

@lru_cache
def get_settings() -> Settings:
    return Settings()
