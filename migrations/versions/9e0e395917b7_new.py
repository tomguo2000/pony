"""new

Revision ID: 9e0e395917b7
Revises: 276ff79ed610
Create Date: 2020-07-18 16:24:57.971545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e0e395917b7'
down_revision = '276ff79ed610'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('ipv6', sa.Boolean(), nullable=True))
    op.add_column('routes', sa.Column('onlineUserAmount', sa.Integer(), nullable=True))
    op.add_column('routes', sa.Column('trojanVersion', sa.String(length=100), nullable=True))
    op.drop_constraint('routes_ibfk_1', 'routes', type_='foreignkey')
    op.add_column('usergroup', sa.Column('maxPwdCapacity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usergroup', 'maxPwdCapacity')
    op.create_foreign_key('routes_ibfk_1', 'routes', 'usergroup', ['usergroup_id'], ['id'])
    op.drop_column('routes', 'trojanVersion')
    op.drop_column('routes', 'onlineUserAmount')
    op.drop_column('routes', 'ipv6')
    # ### end Alembic commands ###