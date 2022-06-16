"""redo all relationships

Revision ID: 1c36ad205af9
Revises: b796cfda598e
Create Date: 2022-06-16 09:30:05.914794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c36ad205af9'
down_revision = 'b796cfda598e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family_association',
    sa.Column('parent_email', sa.String(), nullable=True),
    sa.Column('student_email', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_email'], ['parents.email'], ),
    sa.ForeignKeyConstraint(['student_email'], ['students.email'], ),
    sa.UniqueConstraint('parent_email'),
    sa.UniqueConstraint('student_email')
    )
    op.add_column('edu_phases', sa.Column('edu_stage_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'edu_phases', 'edu_stages', ['edu_stage_id'], ['id'], ondelete='CASCADE')
    op.add_column('edu_stages', sa.Column('school_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'edu_stages', 'schools', ['school_id'], ['id'], ondelete='CASCADE')
    op.add_column('grades', sa.Column('edu_phase_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'grades', 'edu_phases', ['edu_phase_id'], ['id'], ondelete='CASCADE')
    op.add_column('managers', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'managers', ['user_id'])
    op.create_foreign_key(None, 'managers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('parents', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'parents', ['email'])
    op.create_foreign_key(None, 'parents', 'users', ['email'], ['email'], ondelete='CASCADE')
    op.add_column('schools', sa.Column('manager_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'schools', ['manager_id'])
    op.create_foreign_key(None, 'schools', 'managers', ['manager_id'], ['user_id'])
    op.add_column('staff', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'staff', ['email'])
    op.create_foreign_key(None, 'staff', 'users', ['email'], ['email'], ondelete='CASCADE')
    op.add_column('students', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'students', ['email'])
    op.create_foreign_key(None, 'students', 'users', ['email'], ['email'], ondelete='CASCADE')
    op.add_column('users', sa.Column('school_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'schools', ['school_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'school_id')
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_constraint(None, 'students', type_='unique')
    op.drop_column('students', 'email')
    op.drop_constraint(None, 'staff', type_='foreignkey')
    op.drop_constraint(None, 'staff', type_='unique')
    op.drop_column('staff', 'email')
    op.drop_constraint(None, 'schools', type_='foreignkey')
    op.drop_constraint(None, 'schools', type_='unique')
    op.drop_column('schools', 'manager_id')
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.drop_constraint(None, 'parents', type_='unique')
    op.drop_column('parents', 'email')
    op.drop_constraint(None, 'managers', type_='foreignkey')
    op.drop_constraint(None, 'managers', type_='unique')
    op.drop_column('managers', 'user_id')
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.drop_column('grades', 'edu_phase_id')
    op.drop_constraint(None, 'edu_stages', type_='foreignkey')
    op.drop_column('edu_stages', 'school_id')
    op.drop_constraint(None, 'edu_phases', type_='foreignkey')
    op.drop_column('edu_phases', 'edu_stage_id')
    op.drop_table('family_association')
    # ### end Alembic commands ###