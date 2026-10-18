"""Create cold_rooms table."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_cold_rooms"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cold_rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("commodity", sa.String(length=100), nullable=False),
        sa.Column("target_min_c", sa.Float(), nullable=False, server_default="2.0"),
        sa.Column("target_max_c", sa.Float(), nullable=False, server_default="8.0"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_cold_rooms_id", "cold_rooms", ["id"])
    op.create_index("ix_cold_rooms_name", "cold_rooms", ["name"])


def downgrade() -> None:
    op.drop_index("ix_cold_rooms_name", table_name="cold_rooms")
    op.drop_index("ix_cold_rooms_id", table_name="cold_rooms")
    op.drop_table("cold_rooms")
