"""add content column to table

Revision ID: 7f4790b0c099
Revises: 50e3045272fe
Create Date: 2025-02-17 14:32:54.103628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f4790b0c099'
down_revision: Union[str, None] = '50e3045272fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
