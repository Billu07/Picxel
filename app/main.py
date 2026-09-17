"""ASGI entry point (``uvicorn app.main:app``), used by ``picxel serve`` and ``picxel dev``."""

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.factory import create_app

settings = get_settings()
configure_logging(settings.log_level, json_output=settings.is_deployed)
app = create_app(settings)
