"""db models typo fix

Revision ID: cd144e78ede8
Revises: 33d7b2530e4f
Create Date: 2022-05-27 13:49:20.689505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd144e78ede8'
down_revision = '33d7b2530e4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('edu_phases', sa.Column('edu_stage_id', sa.Integer(), nullable=False))
    op.drop_constraint('edu_phases_edu_stage_fkey', 'edu_phases', type_='foreignkey')
    op.create_foreign_key(None, 'edu_phases', 'edu_stages', ['edu_stage_id'], ['id'], ondelete='CASCADE')
    op.drop_column('edu_phases', 'edu_stage')
    op.add_column('grades', sa.Column('edu_phase_id', sa.Integer(), nullable=False))
    op.drop_constraint('grades_edu_phase_fkey', 'grades', type_='foreignkey')
    op.create_foreign_key(None, 'grades', 'edu_phases', ['edu_phase_id'], ['id'], ondelete='CASCADE')
    op.drop_column('grades', 'edu_phase')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('edu_phase', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.create_foreign_key('grades_edu_phase_fkey', 'grades', 'edu_phases', ['edu_phase'], ['id'], ondelete='CASCADE')
    op.drop_column('grades', 'edu_phase_id')
    op.add_column('edu_phases', sa.Column('edu_stage', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'edu_phases', type_='foreignkey')
    op.create_foreign_key('edu_phases_edu_stage_fkey', 'edu_phases', 'edu_stages', ['edu_stage'], ['id'], ondelete='CASCADE')
    op.drop_column('edu_phases', 'edu_stage_id')
    # ### end Alembic commands ###