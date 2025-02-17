"""drop tables

Revision ID: f7d4435625d1
Revises: 68072cc9367c
Create Date: 2025-02-17 17:34:12.377730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7d4435625d1'
down_revision: Union[str, None] = '68072cc9367c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
