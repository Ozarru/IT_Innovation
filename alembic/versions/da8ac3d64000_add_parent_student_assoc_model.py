"""add parent_student_assoc model

Revision ID: da8ac3d64000
Revises: 0db91d4fe895
Create Date: 2022-06-15 09:46:56.988964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8ac3d64000'
down_revision = '0db91d4fe895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent_student_assoc',
    sa.Column('parent_email', sa.String(), nullable=True),
    sa.Column('student_email', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_email'], ['parents.email'], ),
    sa.ForeignKeyConstraint(['student_email'], ['students.email'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parent_student_assoc')
    # ### end Alembic commands ###