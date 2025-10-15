"""added default states to created_at and updated_at

Revision ID: b34022b4b685
Revises: 68e0a0d1cdb6
Create Date: 2025-10-15 13:34:50.536438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b34022b4b685'
down_revision: Union[str, Sequence[str], None] = '68e0a0d1cdb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands manually added to set server defaults for timestamp columns ###
    op.alter_column(
        'warehouses', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'warehouses', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'zones', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'zones', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'aisles', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'aisles', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'racks', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'racks', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'bins', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'bins', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'bin_positions', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'bin_positions', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'pallets', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'pallets', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )

    op.alter_column(
        'pallet_stock', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    op.alter_column(
        'pallet_stock', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')
    )
    # ### end manual commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands manually added to remove server defaults ###
    op.alter_column(
        'warehouses', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'warehouses', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'zones', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'zones', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'aisles', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'aisles', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'racks', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'racks', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'bins', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'bins', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'bin_positions', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'bin_positions', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'pallets', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'pallets', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )

    op.alter_column(
        'pallet_stock', 'created_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    op.alter_column(
        'pallet_stock', 'updated_at',
        existing_type=sa.DateTime(), existing_nullable=False,
        server_default=None
    )
    # ### end manual commands ###
