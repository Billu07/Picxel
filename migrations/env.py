"""Alembic migration environment."""

import logging

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_settings, to_sqlalchemy_url
from app.db.base import Base

config = context.config
target_metadata = Base.metadata

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(name)s: %(message)s")


def _database_url() -> str:
    """Prefer a URL set by the caller (``picxel migrate``, tests); fall back to settings."""
    url = config.get_main_option("sqlalchemy.url") or get_settings().sqlalchemy_database_url
    if not url:
        raise RuntimeError("Set PICXEL_DATABASE_URL to run migrations.")
    return to_sqlalchemy_url(url)


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": _database_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
