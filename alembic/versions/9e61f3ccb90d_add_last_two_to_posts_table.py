"""add last two to posts table

Revision ID: 9e61f3ccb90d
Revises: c49b9ecd1c19
Create Date: 2025-02-04 15:21:23.498612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e61f3ccb90d'
down_revision: Union[str, None] = 'c49b9ecd1c19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),
                                    nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text
                                    ('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts',"published")
    op.drop_column('posts', 'created_at')
    pass
