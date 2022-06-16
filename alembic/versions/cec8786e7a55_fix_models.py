"""fix models

Revision ID: cec8786e7a55
Revises: 046a5dcc7dcd
Create Date: 2022-06-15 14:39:40.001097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cec8786e7a55'
down_revision = '046a5dcc7dcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('matric_id', sa.Integer(), nullable=False),
    sa.Column('is_staff', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['email'], ['users.email'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('matric_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff')
    # ### end Alembic commands ###