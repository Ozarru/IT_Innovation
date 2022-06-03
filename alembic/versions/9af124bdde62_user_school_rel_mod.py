"""user-school rel. mod

Revision ID: 9af124bdde62
Revises: c32fb7845cc3
Create Date: 2022-05-30 14:44:23.915146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af124bdde62'
down_revision = 'c32fb7845cc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schools', sa.Column('admin_id', sa.Integer(), server_default='2', nullable=False))
    op.create_foreign_key(None, 'schools', 'users', ['admin_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schools', type_='foreignkey')
    op.drop_column('schools', 'admin_id')
    # ### end Alembic commands ###
