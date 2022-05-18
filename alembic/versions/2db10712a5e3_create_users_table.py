"""create users table

Revision ID: 2db10712a5e3
Revises: 
Create Date: 2022-05-17 08:16:03.468011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2db10712a5e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              primary_key=True, unique=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(),
                              unique=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(), nullable=True),
                    sa.Column('address', sa.String(), nullable=True),
                    sa.Column('is_student', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('is_parent', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('is_staff', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('is_owner', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('is_admin', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('is_super_admin', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('admin_level', sa.Integer(),
                              server_default=sa.text('0'), nullable=False),
                    sa.Column('registered_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )


def downgrade():
    op.drop_table('users')
