"""manager-user-school  rel.

Revision ID: b7ed3b16a211
Revises: 0eb9bb6fe094
Create Date: 2022-05-30 18:18:46.955247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7ed3b16a211'
down_revision = '0eb9bb6fe094'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schools', sa.Column('manager_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'schools', 'managers', ['manager_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schools', type_='foreignkey')
    op.drop_column('schools', 'manager_id')
    # ### end Alembic commands ###