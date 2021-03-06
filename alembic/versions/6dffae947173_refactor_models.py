"""refactor  models

Revision ID: 6dffae947173
Revises: 83188c4d8da9
Create Date: 2022-07-08 09:57:22.996256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dffae947173'
down_revision = '83188c4d8da9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assoc_payment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assoc_payment',
    sa.Column('payment_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('student_matric', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], name='assoc_payment_payment_id_fkey'),
    sa.ForeignKeyConstraint(['student_matric'], ['students.matric_id'], name='assoc_payment_student_matric_fkey'),
    sa.UniqueConstraint('payment_id', name='assoc_payment_payment_id_key'),
    sa.UniqueConstraint('student_matric', name='assoc_payment_student_matric_key')
    )
    # ### end Alembic commands ###
