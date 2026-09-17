from fastapi.testclient import TestClient

from app.factory import create_app
from tests.factories import make_settings


def test_liveness_is_always_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_without_a_database(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "not_configured"}}


def test_readiness_reports_an_unreachable_database() -> None:
    settings = make_settings(database_url="postgresql://picxel:picxel@127.0.0.1:9/picxel")

    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "checks": {"database": "error"}}


def test_version_reports_build_metadata() -> None:
    settings = make_settings(git_sha="abc1234", build_time="2026-09-14T00:00:00Z")

    with TestClient(create_app(settings)) as client:
        body = client.get("/api/v1/version").json()

    assert body["name"] == "picxel"
    assert body["version"]
    assert body["git_sha"] == "abc1234"
    assert body["build_time"] == "2026-09-14T00:00:00Z"
    assert body["environment"] == "test"
    assert body["models"] == []
