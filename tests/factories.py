"""Test helpers shared across test modules."""

from typing import Any

from app.core.config import Settings


def make_settings(**overrides: Any) -> Settings:
    """Settings isolated from the developer's environment variables and ``.env`` file."""
    values: dict[str, Any] = {"env": "test", "database_url": None} | overrides
    return Settings(_env_file=None, **values)
