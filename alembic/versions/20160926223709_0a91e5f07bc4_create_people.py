"""Create people

Revision ID: 0a91e5f07bc4
Revises:
Create Date: 2016-09-26 22:37:09.602287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '0a91e5f07bc4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('people',
                    sa.Column('id', sa.Integer(), nullable=False, index=True),
                    sa.Column('email', sa.String(length=50), nullable=True,
                              index=True, unique=True),
                    sa.Column('phone', sa.String(length=20), nullable=True,
                              index=True, unique=True),
                    sa.Column('account_id', sa.String(length=20),
                              nullable=True, index=True, unique=True),
                    sa.Column('name', sa.String(length=50), nullable=True,
                              index=True),
                    sa.Column('created_at', sa.DateTime, nullable=False,
                              server_default=func.now()),
                    sa.Column('updated_at', sa.DateTime, nullable=False,
                              server_onupdate=func.now(),
                              server_default=func.now()),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('people')
