import pytest

from app.core.config import Environment, to_sqlalchemy_url
from tests.factories import make_settings


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("postgres://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        (
            "postgresql://u:p@host/db?sslmode=require",
            "postgresql+psycopg://u:p@host/db?sslmode=require",
        ),
        ("postgresql+psycopg://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
    ],
)
def test_postgres_urls_use_the_psycopg_driver(url: str, expected: str) -> None:
    assert to_sqlalchemy_url(url) == expected


def test_blank_database_url_means_not_configured() -> None:
    assert make_settings(database_url="").sqlalchemy_database_url is None


def test_blank_build_time_means_unknown() -> None:
    assert make_settings(build_time="").build_time is None


def test_database_url_is_hidden_from_repr() -> None:
    settings = make_settings(database_url="postgresql://picxel:hunter2@db.example/picxel")

    assert "hunter2" not in repr(settings)
    assert (
        settings.sqlalchemy_database_url == "postgresql+psycopg://picxel:hunter2@db.example/picxel"
    )


@pytest.mark.parametrize(
    ("env", "deployed"),
    [("local", False), ("test", False), ("staging", True), ("production", True)],
)
def test_only_staging_and_production_are_deployed(env: Environment, deployed: bool) -> None:
    assert make_settings(env=env).is_deployed is deployed
