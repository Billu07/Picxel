"""Tests against a real PostgreSQL. Skipped unless PICXEL_TEST_DATABASE_URL is set (CI sets it)."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.core.config import to_sqlalchemy_url
from app.db.migrations import upgrade_to_head
from app.factory import create_app
from tests.factories import make_settings

TEST_DATABASE_URL = os.environ.get("PICXEL_TEST_DATABASE_URL", "")

pytestmark = [
    pytest.mark.db,
    pytest.mark.skipif(not TEST_DATABASE_URL, reason="PICXEL_TEST_DATABASE_URL is not set"),
]


def test_migrations_upgrade_to_head() -> None:
    url = to_sqlalchemy_url(TEST_DATABASE_URL)

    upgrade_to_head(url)

    engine = create_engine(url)
    try:
        with engine.connect() as connection:
            revision = connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one()
    finally:
        engine.dispose()
    assert revision == "0001"


def test_readiness_with_a_reachable_database() -> None:
    with TestClient(create_app(make_settings(database_url=TEST_DATABASE_URL))) as client:
        response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok"}}
