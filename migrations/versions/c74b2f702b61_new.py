"""new

Revision ID: c74b2f702b61
Revises: 6caa4d8275e0
Create Date: 2020-05-04 23:19:39.028190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c74b2f702b61'
down_revision = '6caa4d8275e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'pwresources', 'usergroup', ['usergroup_id'], ['id'])
    op.create_foreign_key(None, 'routes', 'usergroup', ['usergroup_id'], ['id'])
    op.create_foreign_key(None, 'user', 'usergroup', ['usergroup_id'], ['id'])
    op.create_foreign_key(None, 'user', 'thunderservice', ['thunderservice_id'], ['id'])
    op.add_column('usergroup', sa.Column('which_thunderservice', sa.Integer(), nullable=True))
    op.drop_column('usergroup', 'thunderservice_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usergroup', sa.Column('thunderservice_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('usergroup', 'which_thunderservice')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'routes', type_='foreignkey')
    op.drop_constraint(None, 'pwresources', type_='foreignkey')
    # ### end Alembic commands ###
