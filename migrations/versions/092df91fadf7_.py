"""empty message

Revision ID: 092df91fadf7
Revises: 452212c1cce1
Create Date: 2019-08-24 07:42:25.803800

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '092df91fadf7'
down_revision = '452212c1cce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ampc_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('project_name', sa.String(length=120), nullable=False),
        sa.Column('dataset', sa.String(length=40), nullable=False),
        sa.Column('model_type', sa.String(length=120), nullable=False),
        sa.Column('normalization', sa.Boolean(), nullable=True),
        sa.Column('trained_model', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ampc_data')
    # ### end Alembic commands ###
