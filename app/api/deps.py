"""Shared FastAPI dependencies."""

from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy import Engine

from app.core.config import Settings


def settings_from_app(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


def engine_from_app(request: Request) -> Engine | None:
    return cast(Engine | None, request.app.state.db_engine)


SettingsDep = Annotated[Settings, Depends(settings_from_app)]
EngineDep = Annotated[Engine | None, Depends(engine_from_app)]
