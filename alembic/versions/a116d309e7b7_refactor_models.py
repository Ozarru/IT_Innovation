"""refactor  models

Revision ID: a116d309e7b7
Revises: 6dffae947173
Create Date: 2022-07-08 10:11:17.330673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a116d309e7b7'
down_revision = '6dffae947173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('classes', 'class_size',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('classes', 'class_size',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###