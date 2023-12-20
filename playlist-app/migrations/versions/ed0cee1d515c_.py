"""empty message

Revision ID: ed0cee1d515c
Revises: 
Create Date: 2023-12-14 11:12:31.575695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed0cee1d515c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_column('artist')

    # ### end Alembic commands ###
