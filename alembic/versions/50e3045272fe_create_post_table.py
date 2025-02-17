"""create post table

Revision ID: 50e3045272fe
Revises: 
Create Date: 2025-02-17 12:54:07.118180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50e3045272fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String,nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
