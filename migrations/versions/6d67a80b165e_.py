"""empty message

Revision ID: 6d67a80b165e
Revises: 4d818be2aaa8
Create Date: 2021-06-14 03:13:33.423986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d67a80b165e'
down_revision = '4d818be2aaa8'
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
    sa.Column('uploads_path', sa.String(length=64), nullable=True),
    sa.Column('avatar_file', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_avatar_file'), ['avatar_file'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_uploads_path'), ['uploads_path'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=16), nullable=True),
    sa.Column('about', sa.String(length=140), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_company_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_company_phone'), ['phone'], unique=False)

    op.create_table('doctor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=16), nullable=True),
    sa.Column('clinic', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doctor_clinic'), ['clinic'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctor_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctor_middle_name'), ['middle_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctor_phone'), ['phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctor_second_name'), ['second_name'], unique=False)

    op.create_table('worker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('license', sa.String(length=10), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('birth', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('uploads_path', sa.String(length=64), nullable=True),
    sa.Column('avatar_file', sa.String(length=64), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_worker_avatar_file'), ['avatar_file'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_license'), ['license'], unique=True)
        batch_op.create_index(batch_op.f('ix_worker_middle_name'), ['middle_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_second_name'), ['second_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_uploads_path'), ['uploads_path'], unique=True)

    op.create_table('examination',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Numeric(precision=2, scale=1), nullable=True),
    sa.Column('pulse', sa.Integer(), nullable=True),
    sa.Column('blood_pressure', sa.String(length=10), nullable=True),
    sa.Column('alcohol_level', sa.Numeric(precision=1, scale=2), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('close_time', sa.DateTime(), nullable=True),
    sa.Column('close_status', sa.Boolean(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('worker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.Column('unread_exams', sa.Integer(), nullable=True),
    sa.Column('close_exam', sa.Boolean(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['exam_id'], ['examination.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_date'), ['date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_date'))

    op.drop_table('message')
    op.drop_table('examination')
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_worker_uploads_path'))
        batch_op.drop_index(batch_op.f('ix_worker_second_name'))
        batch_op.drop_index(batch_op.f('ix_worker_middle_name'))
        batch_op.drop_index(batch_op.f('ix_worker_license'))
        batch_op.drop_index(batch_op.f('ix_worker_first_name'))
        batch_op.drop_index(batch_op.f('ix_worker_email'))
        batch_op.drop_index(batch_op.f('ix_worker_avatar_file'))

    op.drop_table('worker')
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doctor_second_name'))
        batch_op.drop_index(batch_op.f('ix_doctor_phone'))
        batch_op.drop_index(batch_op.f('ix_doctor_middle_name'))
        batch_op.drop_index(batch_op.f('ix_doctor_first_name'))
        batch_op.drop_index(batch_op.f('ix_doctor_clinic'))

    op.drop_table('doctor')
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_company_phone'))
        batch_op.drop_index(batch_op.f('ix_company_name'))

    op.drop_table('company')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_uploads_path'))
        batch_op.drop_index(batch_op.f('ix_user_role'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_avatar_file'))

    op.drop_table('user')
    # ### end Alembic commands ###