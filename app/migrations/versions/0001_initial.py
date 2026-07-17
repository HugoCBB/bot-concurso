"""initial schema: contests + editais

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fingerprint", sa.String(length=32), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="pciconcursos"),
        sa.Column("orgao", sa.String(length=255), nullable=False),
        sa.Column("info", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("cargo", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("nivel", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("data_limite", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("link", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_contests_fingerprint", "contests", ["fingerprint"], unique=True)
    op.create_index("ix_contests_source", "contests", ["source"], unique=False)

    op.create_table(
        "editais",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("contest_id", sa.Integer(), nullable=False),
        sa.Column("s3_url", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["contest_id"], ["contests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_editais_contest_id", "editais", ["contest_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_editais_contest_id", table_name="editais")
    op.drop_table("editais")
    op.drop_index("ix_contests_source", table_name="contests")
    op.drop_index("ix_contests_fingerprint", table_name="contests")
    op.drop_table("contests")
