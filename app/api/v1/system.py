"""System endpoints: liveness and readiness probes, plus build and model versions."""

from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import Engine

from app.api.deps import EngineDep, SettingsDep
from app.core.meta import PROJECT_NAME, package_version
from app.db.session import database_is_reachable

router = APIRouter(tags=["system"])

CheckResult = Literal["ok", "not_configured", "error"]


class Liveness(BaseModel):
    status: Literal["ok"]


class Readiness(BaseModel):
    status: Literal["ok", "degraded"]
    checks: dict[str, CheckResult]


class ModelInfo(BaseModel):
    name: str
    version: str


class VersionInfo(BaseModel):
    name: str
    version: str
    git_sha: str
    build_time: str | None
    environment: str
    models: list[ModelInfo]


@router.get("/health", summary="Liveness probe")
async def liveness() -> Liveness:
    """200 whenever the process can serve requests. Never touches dependencies."""
    return Liveness(status="ok")


@router.get(
    "/health/ready",
    summary="Readiness probe",
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": Readiness}},
)
def readiness(engine: EngineDep, response: Response) -> Readiness:
    """Checks dependencies. Sync on purpose: the blocking database ping runs in a worker thread."""
    database = _database_check(engine)
    if database == "error":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Readiness(status="degraded", checks={"database": database})
    return Readiness(status="ok", checks={"database": database})


@router.get("/version", summary="Build and model versions")
async def version(settings: SettingsDep) -> VersionInfo:
    return VersionInfo(
        name=PROJECT_NAME,
        version=package_version(),
        git_sha=settings.git_sha,
        build_time=settings.build_time,
        environment=settings.env,
        models=[],  # filled from models/registry.yaml once the detector ships (Phase 1)
    )


def _database_check(engine: Engine | None) -> CheckResult:
    if engine is None:
        return "not_configured"
    return "ok" if database_is_reachable(engine) else "error"
