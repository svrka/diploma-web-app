"""close exam message

Revision ID: dd111df7a5cc
Revises: 60fb259aa0bb
Create Date: 2021-06-12 00:05:03.010772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd111df7a5cc'
down_revision = '60fb259aa0bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('close_exam', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('close_exam')

    # ### end Alembic commands ###
