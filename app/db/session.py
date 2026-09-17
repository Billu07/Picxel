"""Database engine.

Picxel uses SQLAlchemy's synchronous engine with psycopg 3 (decision.md D-005): database work here
is small and infrequent, sync code works on every platform's event loop (psycopg's async mode can't
run on Windows' default loop), and Alembic shares the same driver.
"""

import logging

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def create_db_engine(url: str) -> Engine:
    """Create a lazily-connecting engine tuned for Neon's serverless Postgres."""
    return create_engine(
        url,
        pool_pre_ping=True,  # Neon scales compute to zero; transparently replace dead connections
        pool_size=5,
        max_overflow=5,
        pool_recycle=300,
        connect_args={
            "connect_timeout": 5,
            # No server-side prepared statements: stays compatible with Neon's PgBouncer pooler.
            "prepare_threshold": None,
        },
    )


def database_is_reachable(engine: Engine) -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Database readiness check failed", exc_info=True)
        return False
    return True
