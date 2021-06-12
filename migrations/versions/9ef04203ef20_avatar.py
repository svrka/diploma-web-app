"""avatar

Revision ID: 9ef04203ef20
Revises: dd111df7a5cc
Create Date: 2021-06-12 06:06:14.347089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef04203ef20'
down_revision = 'dd111df7a5cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_avatar'), ['avatar'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_avatar'))
        batch_op.drop_column('avatar')

    # ### end Alembic commands ###
