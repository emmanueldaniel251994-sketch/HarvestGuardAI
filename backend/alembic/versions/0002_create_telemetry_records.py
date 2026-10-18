"""Create telemetry_records table."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_telemetry_records"
down_revision: Union[str, None] = "0001_cold_rooms"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "telemetry_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cold_room_id", sa.Integer(), sa.ForeignKey("cold_rooms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("temperature_c", sa.Float(), nullable=False),
        sa.Column("humidity_pct", sa.Float(), nullable=False),
        sa.Column("battery_pct", sa.Float(), nullable=False),
        sa.Column("solar_power_w", sa.Float(), nullable=False),
        sa.Column("load_power_w", sa.Float(), nullable=False),
    )
    op.create_index("ix_telemetry_records_id", "telemetry_records", ["id"])
    op.create_index("ix_telemetry_records_cold_room_id", "telemetry_records", ["cold_room_id"])
    op.create_index("ix_telemetry_records_timestamp", "telemetry_records", ["timestamp"])


def downgrade() -> None:
    op.drop_index("ix_telemetry_records_timestamp", table_name="telemetry_records")
    op.drop_index("ix_telemetry_records_cold_room_id", table_name="telemetry_records")
    op.drop_index("ix_telemetry_records_id", table_name="telemetry_records")
    op.drop_table("telemetry_records")
