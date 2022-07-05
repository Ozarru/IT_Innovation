"""fix associations

Revision ID: 9c5a1c396fd9
Revises: 651f6801b81c
Create Date: 2022-07-03 21:33:49.350132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9c5a1c396fd9'
down_revision = '651f6801b81c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timetables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.Column('term_id', sa.Integer(), nullable=False),
    sa.Column('academic_year_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['academic_year_id'], ['academic_years.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['grade_id'], ['grades.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('academic_days',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.Column('timetable_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['timetable_id'], ['timetables.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_parent',
    sa.Column('parent_email', sa.String(), nullable=True),
    sa.Column('student_email', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_email'], ['parents.email'], ),
    sa.ForeignKeyConstraint(['student_email'], ['students.email'], ),
    sa.UniqueConstraint('parent_email'),
    sa.UniqueConstraint('student_email')
    )
    op.create_table('exam_days',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.Column('timetable_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['timetable_id'], ['timetables.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fee_id', sa.Integer(), nullable=False),
    sa.Column('amount_payed', sa.Integer(), nullable=False),
    sa.Column('amount_due', sa.Integer(), server_default='0', nullable=True),
    sa.ForeignKeyConstraint(['fee_id'], ['fees.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('periods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.Column('academic_day_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['academic_day_id'], ['timetables.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'subject_id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('subject_id')
    )
    op.create_table('association_payment',
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('student_matric', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], ),
    sa.UniqueConstraint('payment_id'),
    sa.UniqueConstraint('student_matric')
    )
    op.create_table('class_attendances',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_present', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('remark', sa.String(), nullable=True),
    sa.Column('period_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['period_id'], ['periods.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_class_attendance',
    sa.Column('attendance_id', sa.Integer(), nullable=True),
    sa.Column('student_matric', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attendance_id'], ['class_attendances.id'], ),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], ),
    sa.UniqueConstraint('attendance_id'),
    sa.UniqueConstraint('student_matric')
    )
    op.create_table('exam_attendances',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_present', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('remark', sa.String(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'exam_id'),
    sa.UniqueConstraint('exam_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('exam_grades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('score', sa.Float(), server_default='0', nullable=True),
    sa.Column('remark', sa.String(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'exam_id'),
    sa.UniqueConstraint('exam_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('exam_stats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('candidates', sa.Integer(), server_default='0', nullable=True),
    sa.Column('highest_score', sa.Float(), server_default='0', nullable=True),
    sa.Column('lowest_score', sa.Float(), server_default='0', nullable=True),
    sa.Column('average_score', sa.Float(), server_default='0', nullable=True),
    sa.Column('success_rate', sa.Float(), server_default='0', nullable=True),
    sa.Column('failure_rate', sa.Float(), server_default='0', nullable=True),
    sa.Column('observations', sa.String(), server_default='Nothing to report', nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'exam_id'),
    sa.UniqueConstraint('exam_id')
    )
    op.create_table('association_exam_attendance',
    sa.Column('attendance_id', sa.Integer(), nullable=True),
    sa.Column('student_matric', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attendance_id'], ['exam_attendances.id'], ),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], ),
    sa.UniqueConstraint('attendance_id'),
    sa.UniqueConstraint('student_matric')
    )
    op.create_table('association_exam_grades',
    sa.Column('exam_grade_id', sa.Integer(), nullable=True),
    sa.Column('student_matric', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_grade_id'], ['exam_grades.id'], ),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], ),
    sa.UniqueConstraint('exam_grade_id'),
    sa.UniqueConstraint('student_matric')
    )
    op.drop_table('class_attendance')
    op.drop_table('family_association')
    op.add_column('exams', sa.Column('name', sa.String(), nullable=True))
    op.add_column('exams', sa.Column('duration', sa.Float(), nullable=False))
    op.add_column('exams', sa.Column('start_time', sa.String(), nullable=False))
    op.add_column('exams', sa.Column('end_time', sa.String(), nullable=False))
    op.add_column('exams', sa.Column('exam_day_id', sa.Integer(), nullable=False))
    op.alter_column('exams', 'genre',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_unique_constraint(None, 'exams', ['id'])
    op.create_foreign_key(None, 'exams', 'exam_days', ['exam_day_id'], ['id'], ondelete='CASCADE')
    op.drop_column('exams', 'observations')
    op.drop_column('exams', 'failure_rate')
    op.drop_column('exams', 'highest_score')
    op.drop_column('exams', 'average_score')
    op.drop_column('exams', 'lowest_score')
    op.drop_column('exams', 'success_rate')
    op.drop_column('exams', 'participants')
    op.add_column('fees', sa.Column('name', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fees', 'name')
    op.add_column('exams', sa.Column('participants', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('success_rate', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('lowest_score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('average_score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('highest_score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('failure_rate', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('exams', sa.Column('observations', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'exams', type_='foreignkey')
    op.drop_constraint(None, 'exams', type_='unique')
    op.alter_column('exams', 'genre',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('exams', 'exam_day_id')
    op.drop_column('exams', 'end_time')
    op.drop_column('exams', 'start_time')
    op.drop_column('exams', 'duration')
    op.drop_column('exams', 'name')
    op.create_table('family_association',
    sa.Column('parent_email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('student_email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_email'], ['parents.email'], name='family_association_parent_email_fkey'),
    sa.ForeignKeyConstraint(['student_email'], ['students.email'], name='family_association_student_email_fkey'),
    sa.UniqueConstraint('parent_email', name='family_association_parent_email_key'),
    sa.UniqueConstraint('student_email', name='family_association_student_email_key')
    )
    op.create_table('class_attendance',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('subject_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('student_matric', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_present', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('remark', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], name='class_attendance_student_matric_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], name='class_attendance_subject_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'subject_id', name='class_attendance_pkey'),
    sa.UniqueConstraint('subject_id', name='class_attendance_subject_id_key')
    )
    op.drop_table('association_exam_grades')
    op.drop_table('association_exam_attendance')
    op.drop_table('exam_stats')
    op.drop_table('exam_grades')
    op.drop_table('exam_attendances')
    op.drop_table('association_class_attendance')
    op.drop_table('class_attendances')
    op.drop_table('association_payment')
    op.drop_table('periods')
    op.drop_table('payments')
    op.drop_table('exam_days')
    op.drop_table('association_parent')
    op.drop_table('academic_days')
    op.drop_table('timetables')
    # ### end Alembic commands ###
