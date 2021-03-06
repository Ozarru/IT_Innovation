"""models refactoring

Revision ID: 450980e94129
Revises: 1c830e228c8b
Create Date: 2022-05-31 10:48:39.486897

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '450980e94129'
down_revision = '1c830e228c8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('schools')
    op.drop_table('edu_stages')
    op.drop_table('managers')
    op.drop_table('roles')
    op.drop_table('users')
    op.drop_table('edu_phases')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('edu_phases',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('edu_phases_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('edu_calendar', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('edu_stage_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['edu_stage_id'], ['edu_stages.id'], name='edu_phases_edu_stage_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='edu_phases_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registered_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('firstname', sa.VARCHAR(), server_default=sa.text("'Teslim'::character varying"), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(), server_default=sa.text("'Balogun'::character varying"), autoincrement=False, nullable=False),
    sa.Column('birth_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('last_login', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('school_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_role_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name='users_school_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('phone', name='users_phone_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('roles_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sec_level', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('managers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('edu_phases_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='users_manager_fk', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='managers_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('edu_stages',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('edu_stages_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('school_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name='edu_stages_school_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='edu_stages_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('schools',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('schools_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('rccm_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('nif_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bank_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('bank_acc_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('bank_acc_num', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('registered_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('manager_id', sa.INTEGER(), server_default=sa.text('2'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], name='schools_manager_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='schools_pkey'),
    sa.UniqueConstraint('email', name='schools_email_key'),
    sa.UniqueConstraint('phone', name='schools_phone_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('alias', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('class_size', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('edu_phase_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['edu_phase_id'], ['edu_phases.id'], name='grades_edu_phase_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='grades_pkey')
    )
    # ### end Alembic commands ###
