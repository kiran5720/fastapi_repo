"""add content column to posts table

Revision ID: 59497e61da3d
Revises: 3f6c3beb4b3d
Create Date: 2025-02-04 12:45:33.463519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59497e61da3d'
down_revision: Union[str, None] = '3f6c3beb4b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
