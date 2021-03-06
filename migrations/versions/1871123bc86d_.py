"""empty message

Revision ID: 1871123bc86d
Revises: 1cddc2d0d5d0
Create Date: 2021-05-25 16:20:17.863284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1871123bc86d'
down_revision = '1cddc2d0d5d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], name=op.f('fk_company_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company'))
    )
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_company_name'), ['name'], unique=False)

    op.create_table('doctor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], name=op.f('fk_doctor_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_doctor'))
    )
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doctor_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctor_second_name'), ['second_name'], unique=False)

    op.create_table('worker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name=op.f('fk_worker_company_id_company')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_worker'))
    )
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_worker_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_worker_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_second_name'), ['second_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_worker_second_name'))
        batch_op.drop_index(batch_op.f('ix_worker_first_name'))
        batch_op.drop_index(batch_op.f('ix_worker_email'))

    op.drop_table('worker')
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doctor_second_name'))
        batch_op.drop_index(batch_op.f('ix_doctor_first_name'))

    op.drop_table('doctor')
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_company_name'))

    op.drop_table('company')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_role'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
