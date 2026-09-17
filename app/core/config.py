"""Application settings, read from ``PICXEL_``-prefixed environment variables (and ``.env``)."""

from functools import cache
from typing import Literal

from pydantic import HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "test", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

_PLAIN_POSTGRES_SCHEMES = ("postgres://", "postgresql://")
_PSYCOPG_SCHEME = "postgresql+psycopg://"


def to_sqlalchemy_url(url: str) -> str:
    """Point plain Postgres URLs (as copied from Neon or Docker) at the psycopg 3 driver."""
    for scheme in _PLAIN_POSTGRES_SCHEMES:
        if url.startswith(scheme):
            return _PSYCOPG_SCHEME + url.removeprefix(scheme)
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PICXEL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Environment = "local"
    public_url: HttpUrl = HttpUrl("http://localhost:8000")
    log_level: LogLevel = "INFO"
    database_url: SecretStr | None = None
    git_sha: str = "unknown"
    build_time: str | None = None

    @field_validator("database_url", "build_time", mode="before")
    @classmethod
    def _blank_means_unset(cls, value: object) -> object:
        return None if value == "" else value

    @property
    def is_deployed(self) -> bool:
        return self.env in ("staging", "production")

    @property
    def sqlalchemy_database_url(self) -> str | None:
        if self.database_url is None:
            return None
        return to_sqlalchemy_url(self.database_url.get_secret_value())


@cache
def get_settings() -> Settings:
    return Settings()
