"""fix  models

Revision ID: 84bcbc42c909
Revises: dc4367110fea
Create Date: 2022-07-06 16:14:36.278282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bcbc42c909'
down_revision = 'dc4367110fea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('matric', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'staff', ['matric'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff', type_='unique')
    op.drop_column('staff', 'matric')
    # ### end Alembic commands ###
