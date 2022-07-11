"""fix  models

Revision ID: 5fa7753c80e0
Revises: 84bcbc42c909
Create Date: 2022-07-06 16:17:14.500812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa7753c80e0'
down_revision = '84bcbc42c909'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('matric', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'staff', ['matric'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff', type_='unique')
    op.drop_column('staff', 'matric')
    # ### end Alembic commands ###