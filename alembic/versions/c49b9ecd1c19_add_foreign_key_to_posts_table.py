"""add foreign key to posts table

Revision ID: c49b9ecd1c19
Revises: 5a336886a4ef
Create Date: 2025-02-04 15:12:44.304337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c49b9ecd1c19'
down_revision: Union[str, None] = '5a336886a4ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
