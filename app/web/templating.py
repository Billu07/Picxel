"""Jinja2 environment shared by pages and error pages."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.core.config import Settings
from app.core.meta import REPOSITORY_URL

WEB_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = WEB_DIR / "templates"
STATIC_DIR = WEB_DIR / "static"


def site_context(request: Request) -> dict[str, Any]:
    settings: Settings = request.app.state.settings
    base_url = str(settings.public_url).rstrip("/")
    return {
        "settings": settings,
        "canonical_url": f"{base_url}{request.url.path}",
        "csp_nonce": getattr(request.state, "csp_nonce", None),
        "request_id": getattr(request.state, "request_id", None),
        "repository_url": REPOSITORY_URL,
        "current_year": datetime.now(UTC).year,
    }


templates = Jinja2Templates(directory=TEMPLATES_DIR, context_processors=[site_context])
