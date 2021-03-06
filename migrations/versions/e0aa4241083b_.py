"""empty message

Revision ID: e0aa4241083b
Revises: 78e418962507
Create Date: 2019-09-01 12:34:38.123506

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e0aa4241083b'
down_revision = '78e418962507'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'apmc_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('project_name', sa.String(length=120), nullable=False),
        sa.Column('dataset', sa.String(length=40), nullable=False),
        sa.Column('model_type', sa.String(length=120), nullable=False),
        sa.Column('normalization', sa.Boolean(), nullable=True),
        sa.Column('trained_model', sa.String(length=40), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.drop_table('ampc_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ampc_data',
        sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('customer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('project_name', mysql.VARCHAR(length=120), nullable=False),
        sa.Column('dataset', mysql.VARCHAR(length=40), nullable=False),
        sa.Column('model_type', mysql.VARCHAR(length=120), nullable=False),
        sa.Column('normalization', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
        sa.Column('trained_model', mysql.VARCHAR(length=40), nullable=True),
        sa.Column('created_at', mysql.DATETIME(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='ampc_data_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='latin1',
        mysql_engine='InnoDB',
    )
    op.drop_table('apmc_data')
    # ### end Alembic commands ###
