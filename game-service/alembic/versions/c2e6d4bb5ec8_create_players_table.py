"""create players table

Revision ID: c2e6d4bb5ec8
Revises: b71ef1fbdc52
Create Date: 2026-07-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2e6d4bb5ec8'
down_revision: Union[str, Sequence[str], None] = 'b71ef1fbdc52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'players',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('table_id', sa.Integer(), nullable=True),
        sa.Column('seat_number', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_id'), 'players', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_players_id'), table_name='players')
    op.drop_table('players')
