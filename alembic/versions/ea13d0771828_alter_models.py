"""alter models

Revision ID: ea13d0771828
Revises: da96a64b3a85
Create Date: 2022-07-04 13:41:00.299571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea13d0771828'
down_revision = 'da96a64b3a85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_exam_grades')
    op.drop_column('exam_attendances', 'is_present')
    op.add_column('exam_grades', sa.Column('student_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'exam_grades', ['student_id'])
    op.create_foreign_key(None, 'exam_grades', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exam_grades', type_='foreignkey')
    op.drop_constraint(None, 'exam_grades', type_='unique')
    op.drop_column('exam_grades', 'student_id')
    op.add_column('exam_attendances', sa.Column('is_present', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.create_table('association_exam_grades',
    sa.Column('exam_grade_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('student_matric', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['exam_grade_id'], ['exam_grades.id'], name='association_exam_grades_exam_grade_id_fkey'),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], name='association_exam_grades_student_matric_fkey'),
    sa.UniqueConstraint('exam_grade_id', name='association_exam_grades_exam_grade_id_key'),
    sa.UniqueConstraint('student_matric', name='association_exam_grades_student_matric_key')
    )
    # ### end Alembic commands ###
