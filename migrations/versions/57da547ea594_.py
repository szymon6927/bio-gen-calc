"""empty message

Revision ID: 57da547ea594
Revises: 806e717d120c
Create Date: 2018-11-18 22:47:04.466469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57da547ea594'
down_revision = '806e717d120c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_activity', sa.Column('module_name', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer_activity', 'module_name')
    # ### end Alembic commands ###
