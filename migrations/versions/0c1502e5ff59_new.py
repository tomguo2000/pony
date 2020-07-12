"""new

Revision ID: 0c1502e5ff59
Revises: 492a3521b7c2
Create Date: 2020-07-02 22:38:17.254112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0c1502e5ff59'
down_revision = '492a3521b7c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_column('logs', 'result')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('result', mysql.VARCHAR(length=1024), nullable=True))
    op.drop_column('logs', 'user_id')
    # ### end Alembic commands ###