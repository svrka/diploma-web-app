"""examination close status

Revision ID: 60fb259aa0bb
Revises: 6928c7161dae
Create Date: 2021-06-11 22:47:51.815497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60fb259aa0bb'
down_revision = '6928c7161dae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('examination', schema=None) as batch_op:
        batch_op.add_column(sa.Column('close_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('examination', schema=None) as batch_op:
        batch_op.drop_column('close_status')

    # ### end Alembic commands ###