"""create schools table

Revision ID: c93b31e4c7d5
Revises: 2db10712a5e3
Create Date: 2022-05-18 08:51:00.865702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c93b31e4c7d5'
down_revision = '2db10712a5e3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('schools',
                    sa.Column('id', sa.Integer(),
                              primary_key=True, unique=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('email', sa.String(),
                              unique=True, nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(), nullable=True),
                    sa.Column('rccm_code', sa.Integer(), nullable=True),
                    sa.Column('nif_code', sa.Integer(), nullable=True),
                    sa.Column('bank_name', sa.String(), nullable=True),
                    sa.Column('bank_acc_name', sa.String(), nullable=True),
                    sa.Column('bank_acc_num', sa.BigInteger(), nullable=True),
                    sa.Column('edu_level', sa.String(), nullable=True),
                    sa.Column('term_alloction', sa.String(), nullable=True),
                    sa.Column('is_accredited', sa.Boolean(),
                              server_default='FALSE', nullable=False),
                    sa.Column('admin_id', sa.Integer(), nullable=False),
                    sa.Column('registered_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )
    op.create_foreign_key('school_users_fk', source_table='schools', referent_table='users', local_cols=[
                          'admin_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('school_users_fk', table_name='schools')
    op.drop_table('schools')
