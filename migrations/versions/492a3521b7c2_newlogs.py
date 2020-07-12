"""newlogs

Revision ID: 492a3521b7c2
Revises: c1a919af5094
Create Date: 2020-06-29 23:46:14.972246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '492a3521b7c2'
down_revision = 'c1a919af5094'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('logtime', sa.String(length=50), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('result', sa.String(length=1024), nullable=True),
    sa.Column('remote_ip', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    # ### end Alembic commands ###