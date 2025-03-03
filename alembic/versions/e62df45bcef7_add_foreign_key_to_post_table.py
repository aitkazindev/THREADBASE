"""add foreign key to post table

Revision ID: e62df45bcef7
Revises: d01ec3fa6858
Create Date: 2025-02-17 15:37:16.385211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62df45bcef7'
down_revision: Union[str, None] = 'd01ec3fa6858'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False, server_default='1'))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    pass
