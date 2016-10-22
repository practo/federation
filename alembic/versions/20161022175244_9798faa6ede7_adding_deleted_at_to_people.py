"""Adding deleted_at to people

Revision ID: 9798faa6ede7
Revises: 0a91e5f07bc4
Create Date: 2016-10-22 17:52:44.149196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9798faa6ede7'
down_revision = '0a91e5f07bc4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('people', sa.Column('deleted_at', sa.DateTime,
                                      default=None, nullable=True))


def downgrade():
    op.drop_column('people', 'deleted_at')
