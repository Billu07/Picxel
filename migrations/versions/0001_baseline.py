"""Baseline: anchors the migration history. Tables arrive with the features that need them.

Revision ID: 0001
Revises:
Create Date: 2026-09-14
"""

from collections.abc import Sequence

revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Nothing to create yet."""


def downgrade() -> None:
    """Nothing to drop."""
