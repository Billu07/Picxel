"""Application factory: wires settings, database, routes, error handling, and middleware."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_v1_router
from app.core.config import Settings, get_settings
from app.core.meta import package_version
from app.core.middleware import RequestContextMiddleware, SecurityHeadersMiddleware
from app.db.session import create_db_engine
from app.errors import EXCEPTION_HANDLERS
from app.web.routes import router as web_router
from app.web.templating import STATIC_DIR


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()
    database_url = settings.sqlalchemy_database_url
    engine = create_db_engine(database_url) if database_url else None

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if engine is not None:
                engine.dispose()

    app = FastAPI(
        title="Picxel",
        summary="See what's really in your pixels.",
        version=package_version(),
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        exception_handlers=EXCEPTION_HANDLERS,
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.db_engine = engine

    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(web_router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # Middleware added last runs first: request context wraps security headers, which wrap the app.
    app.add_middleware(SecurityHeadersMiddleware, hsts=settings.is_deployed)
    app.add_middleware(RequestContextMiddleware)
    return app
