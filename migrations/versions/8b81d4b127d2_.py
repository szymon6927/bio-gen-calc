"""empty message

Revision ID: 8b81d4b127d2
Revises: 1893344efdd5
Create Date: 2020-01-08 17:44:23.334481

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b81d4b127d2'
down_revision = '1893344efdd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=250), nullable=True),
        sa.Column('link', sa.String(length=250), nullable=True),
        sa.Column('pub_date', sa.DateTime(), nullable=True),
        sa.Column('desc', sa.Text(), nullable=True),
        sa.Column('was_published', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'feeds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=250), nullable=True),
        sa.Column('url', sa.String(length=250), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.drop_table('feed')
    op.drop_table('article')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'article',
        sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('title', mysql.VARCHAR(charset='latin1', length=250), nullable=True),
        sa.Column('link', mysql.VARCHAR(charset='latin1', length=250), nullable=True),
        sa.Column('pub_date', mysql.DATETIME(), nullable=True),
        sa.Column('desc', mysql.TEXT(), nullable=True),
        sa.Column('was_published', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
        sa.Column('created_at', mysql.DATETIME(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB',
    )
    op.create_table(
        'feed',
        sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('name', mysql.VARCHAR(length=120), nullable=True),
        sa.Column('url', mysql.VARCHAR(length=120), nullable=True),
        sa.Column('created_at', mysql.DATETIME(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='latin1',
        mysql_engine='InnoDB',
    )
    op.drop_table('feeds')
    op.drop_table('articles')
    # ### end Alembic commands ###
