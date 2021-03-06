"""new

Revision ID: b8b1cba09678
Revises: 5ad2f60df2d1
Create Date: 2020-07-19 23:27:11.719324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8b1cba09678'
down_revision = '5ad2f60df2d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routesDynamicData', sa.Column('cpuUsage', sa.String(length=50), nullable=True))
    op.add_column('routesDynamicData', sa.Column('memUsage', sa.String(length=50), nullable=True))
    op.add_column('routesDynamicData', sa.Column('routeLocalTime', sa.String(length=50), nullable=True))
    op.add_column('routesDynamicData', sa.Column('routeStartTime', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('routesDynamicData', 'routeStartTime')
    op.drop_column('routesDynamicData', 'routeLocalTime')
    op.drop_column('routesDynamicData', 'memUsage')
    op.drop_column('routesDynamicData', 'cpuUsage')
    # ### end Alembic commands ###
