"""new

Revision ID: 4f93a26dca5c
Revises: 4b475eec4144
Create Date: 2020-07-30 13:00:54.449942

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f93a26dca5c'
down_revision = '4b475eec4144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cpuio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('pro', sa.Integer(), nullable=True),
    sa.Column('mem', sa.Integer(), nullable=True),
    sa.Column('addtime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diskio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.Column('write_count', sa.Integer(), nullable=True),
    sa.Column('read_bytes', sa.Integer(), nullable=True),
    sa.Column('write_bytes', sa.Integer(), nullable=True),
    sa.Column('read_time', sa.BigInteger(), nullable=True),
    sa.Column('write_time', sa.BigInteger(), nullable=True),
    sa.Column('addtime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('load_average',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('pro', sa.Float(), nullable=True),
    sa.Column('one', sa.Float(), nullable=True),
    sa.Column('five', sa.Float(), nullable=True),
    sa.Column('fifteen', sa.Float(), nullable=True),
    sa.Column('addtime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('network',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('up', sa.Integer(), nullable=True),
    sa.Column('down', sa.Integer(), nullable=True),
    sa.Column('total_up', sa.Integer(), nullable=True),
    sa.Column('total_down', sa.Integer(), nullable=True),
    sa.Column('up_packets', sa.Integer(), nullable=True),
    sa.Column('down_packets', sa.Integer(), nullable=True),
    sa.Column('addtime', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('routesDynamicData')
    op.add_column('routes', sa.Column('availablePwd', sa.Integer(), nullable=True))
    op.add_column('routes', sa.Column('routeLocalTime', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('routes', 'routeLocalTime')
    op.drop_column('routes', 'availablePwd')
    op.create_table('routesDynamicData',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('route_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('ipaddress', mysql.VARCHAR(length=15), nullable=True),
    sa.Column('onlineUserAmount', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('trafficUsed', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('lastCheckTime', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('cpuUsage', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('memUsage', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('routeLocalTime', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('routeStartTime', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('availablePwd', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('network')
    op.drop_table('load_average')
    op.drop_table('diskio')
    op.drop_table('cpuio')
    # ### end Alembic commands ###
