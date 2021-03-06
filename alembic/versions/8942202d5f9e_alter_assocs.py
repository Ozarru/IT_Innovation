"""alter assocs

Revision ID: 8942202d5f9e
Revises: ea13d0771828
Create Date: 2022-07-04 14:47:27.424857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8942202d5f9e'
down_revision = 'ea13d0771828'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_exam_stats',
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('student_matric', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], ),
    sa.UniqueConstraint('exam_id'),
    sa.UniqueConstraint('student_matric')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_exam_stats')
    # ### end Alembic commands ###
