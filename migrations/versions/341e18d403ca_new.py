"""new

Revision ID: 341e18d403ca
Revises: 0c0dca065a2c
Create Date: 2020-07-18 21:50:46.133595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '341e18d403ca'
down_revision = '0c0dca065a2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('routeExpTime', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('routes', 'routeExpTime')
    # ### end Alembic commands ###
