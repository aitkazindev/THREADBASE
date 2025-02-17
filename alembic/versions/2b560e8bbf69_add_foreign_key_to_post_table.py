"""add foreign key to post table

Revision ID: 2b560e8bbf69
Revises: e62df45bcef7
Create Date: 2025-02-17 15:48:44.511949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b560e8bbf69'
down_revision: Union[str, None] = 'e62df45bcef7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    #

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    #op.drop_column('posts', 'created_at')
    pass
