"""payload json

Revision ID: 6928c7161dae
Revises: 7f801cfec932
Create Date: 2021-06-10 04:09:00.646334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6928c7161dae'
down_revision = '7f801cfec932'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('body')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body', sa.VARCHAR(length=140), nullable=True))

    # ### end Alembic commands ###