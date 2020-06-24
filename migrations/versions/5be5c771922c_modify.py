"""modify

Revision ID: 5be5c771922c
Revises: 0a60b1b1dab4
Create Date: 2020-05-03 23:29:25.470103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5be5c771922c'
down_revision = '0a60b1b1dab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pwresources', sa.Column('usergroup_id', sa.Integer(), nullable=True))
    op.add_column('thunderservice', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('thunderservice', 'price')
    op.drop_column('pwresources', 'usergroup_id')
    # ### end Alembic commands ###