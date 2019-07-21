"""empty message

Revision ID: 82dc2b22b8f3
Revises: 
Create Date: 2019-07-21 15:37:45.561556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82dc2b22b8f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calculations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('module_name', sa.String(length=120), nullable=True),
    sa.Column('user_data', sa.Text(), nullable=True),
    sa.Column('result', sa.Text(), nullable=True),
    sa.Column('ip_address', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('profile_pic', sa.String(length=20), nullable=False),
    sa.Column('login', sa.String(length=25), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=80), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=64), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('slug', sa.String(length=220), nullable=True),
    sa.Column('seo_title', sa.String(length=85), nullable=True),
    sa.Column('seo_desc', sa.String(length=180), nullable=True),
    sa.Column('seo_keywords', sa.String(length=200), nullable=True),
    sa.Column('text', sa.UnicodeText(), nullable=True),
    sa.Column('desc', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('module_name', sa.String(length=120), nullable=True),
    sa.Column('url', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_calculations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.Column('module_name', sa.String(length=120), nullable=True),
    sa.Column('customer_input', sa.Text(), nullable=True),
    sa.Column('result', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer_calculations')
    op.drop_table('customer_activity')
    op.drop_table('pages')
    op.drop_table('customers')
    op.drop_table('calculations')
    # ### end Alembic commands ###
