"""Application settings loaded from environment variables and config files."""

from __future__ import annotations

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings for the gdynia-thermal-db project."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Logging
    log_level: str = "INFO"

    # HTTP
    http_timeout: int = 30
    http_user_agent: str = "gdynia-thermal-db/1.0 (research project)"

    # Directories
    data_dir: Path = Path("data")
    output_dir: Path = Path("outputs")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def external_dir(self) -> Path:
        return self.data_dir / "external"

    @property
    def interim_dir(self) -> Path:
        return self.data_dir / "interim"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def tables_dir(self) -> Path:
        return self.output_dir / "tables"

    @property
    def maps_dir(self) -> Path:
        return self.output_dir / "maps"

    @property
    def logs_dir(self) -> Path:
        return self.output_dir / "logs"


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return the singleton Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
