"""new

Revision ID: 472fa3a00aac
Revises: 4f93a26dca5c
Create Date: 2020-07-30 23:08:18.266954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '472fa3a00aac'
down_revision = '4f93a26dca5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('onlineuseramount',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('online_user_amount', sa.Integer(), nullable=True),
    sa.Column('server_local_time', sa.String(length=50), nullable=True),
    sa.Column('server_start_time', sa.String(length=50), nullable=True),
    sa.Column('addtime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('routes', 'onlineUserAmount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('onlineUserAmount', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('onlineuseramount')
    # ### end Alembic commands ###
