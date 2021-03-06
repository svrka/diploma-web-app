"""-timestamp -last-read +closse-time

Revision ID: b2079f8c1cf3
Revises: 58a088aa3443
Create Date: 2021-06-09 13:46:23.067689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2079f8c1cf3'
down_revision = '58a088aa3443'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('examination', schema=None) as batch_op:
        batch_op.add_column(sa.Column('close_time', sa.DateTime(), nullable=True))

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index('ix_message_timestamp')
        batch_op.drop_column('timestamp')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_message_read_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_message_read_time', sa.DATETIME(), nullable=True))

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.FLOAT(), nullable=True))
        batch_op.create_index('ix_message_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('examination', schema=None) as batch_op:
        batch_op.drop_column('close_time')

    # ### end Alembic commands ###
