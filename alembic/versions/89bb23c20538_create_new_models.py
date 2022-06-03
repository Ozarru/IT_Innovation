"""create new models

Revision ID: 89bb23c20538
Revises: 28196a29ae17
Create Date: 2022-05-31 11:01:48.262818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89bb23c20538'
down_revision = '28196a29ae17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('managers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sec_level', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rccm_code', sa.Integer(), nullable=True),
    sa.Column('nif_code', sa.Integer(), nullable=True),
    sa.Column('bank_name', sa.String(), nullable=True),
    sa.Column('bank_acc_name', sa.String(), nullable=True),
    sa.Column('bank_acc_num', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['managers.user_id'], ),
    sa.PrimaryKeyConstraint('id', 'manager_id'),
    sa.UniqueConstraint('bank_acc_num'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('manager_id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('birth_date', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_login', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('edu_stages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edu_phases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('edu_calendar', sa.String(), nullable=False),
    sa.Column('edu_stage_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['edu_stage_id'], ['edu_stages.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('alias', sa.String(), nullable=True),
    sa.Column('class_size', sa.Integer(), nullable=False),
    sa.Column('edu_phase_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['edu_phase_id'], ['edu_phases.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('edu_phases')
    op.drop_table('edu_stages')
    op.drop_table('users')
    op.drop_table('schools')
    op.drop_table('roles')
    op.drop_table('managers')
    # ### end Alembic commands ###
