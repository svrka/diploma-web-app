"""urnead messages amount

Revision ID: 8283c7ab09eb
Revises: b2079f8c1cf3
Create Date: 2021-06-09 16:33:05.557641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8283c7ab09eb'
down_revision = 'b2079f8c1cf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unread_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('unread_count')

    # ### end Alembic commands ###