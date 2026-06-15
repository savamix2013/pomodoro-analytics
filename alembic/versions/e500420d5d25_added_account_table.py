"""Added account table

Revision ID: e500420d5d25
Revises: 
Create Date: 2026-06-15 23:19:11.254230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e500420d5d25'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Manually adjusted: create lowercase tables matching models
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('pomodoro_count', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop created tables in reverse order
    op.drop_table('tasks')
    op.drop_table('categories')
