"""add columns on post table

Revision ID: 20e1c89e8116
Revises: 2b560e8bbf69
Create Date: 2025-02-17 15:54:29.817712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20e1c89e8116'
down_revision: Union[str, None] = '2b560e8bbf69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    pass
