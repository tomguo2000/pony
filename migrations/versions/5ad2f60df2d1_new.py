"""new

Revision ID: 5ad2f60df2d1
Revises: 341e18d403ca
Create Date: 2020-07-19 23:21:49.564938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ad2f60df2d1'
down_revision = '341e18d403ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routesDynamicData',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('onlineUserAmount', sa.Integer(), nullable=True),
    sa.Column('trafficUsed', sa.Integer(), nullable=True),
    sa.Column('lastCheckTime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routesDynamicData')
    # ### end Alembic commands ###
