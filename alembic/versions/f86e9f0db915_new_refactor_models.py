"""new refactor models

Revision ID: f86e9f0db915
Revises: 7cee3c16ac25
Create Date: 2022-07-05 16:01:31.417271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f86e9f0db915'
down_revision = '7cee3c16ac25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('semesters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date', sa.String(), nullable=False),
    sa.Column('end_date', sa.String(), nullable=False),
    sa.Column('term_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trimesters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date', sa.String(), nullable=False),
    sa.Column('end_date', sa.String(), nullable=False),
    sa.Column('term_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('alias', sa.String(), nullable=True),
    sa.Column('class_size', sa.Integer(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.Column('supervisor_mail', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['grades.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['supervisor_mail'], ['staff.email'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('edu_phases', 'edu_calendar')
    op.drop_constraint('edu_stages_school_id_fkey', 'edu_stages', type_='foreignkey')
    op.drop_column('edu_stages', 'school_id')
    op.drop_constraint('grades_supervisor_mail_fkey', 'grades', type_='foreignkey')
    op.drop_column('grades', 'alias')
    op.drop_column('grades', 'supervisor_mail')
    op.drop_column('grades', 'class_size')
    op.add_column('terms', sa.Column('genre', sa.String(), nullable=False))
    op.drop_constraint('terms_edu_phase_id_fkey', 'terms', type_='foreignkey')
    op.drop_column('terms', 'start_date')
    op.drop_column('terms', 'end_date')
    op.drop_column('terms', 'edu_phase_id')
    op.drop_column('terms', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('terms', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('terms', sa.Column('edu_phase_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('terms', sa.Column('end_date', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('terms', sa.Column('start_date', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('terms_edu_phase_id_fkey', 'terms', 'edu_phases', ['edu_phase_id'], ['id'], ondelete='CASCADE')
    op.drop_column('terms', 'genre')
    op.add_column('grades', sa.Column('class_size', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('grades', sa.Column('supervisor_mail', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('grades', sa.Column('alias', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('grades_supervisor_mail_fkey', 'grades', 'staff', ['supervisor_mail'], ['email'], ondelete='CASCADE')
    op.add_column('edu_stages', sa.Column('school_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('edu_stages_school_id_fkey', 'edu_stages', 'schools', ['school_id'], ['id'], ondelete='CASCADE')
    op.add_column('edu_phases', sa.Column('edu_calendar', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_table('classes')
    op.drop_table('trimesters')
    op.drop_table('semesters')
    # ### end Alembic commands ###
