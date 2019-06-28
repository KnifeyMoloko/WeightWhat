"""migr19

Revision ID: 4ff7a6bf2ea0
Revises: 38d5e65972ed
Create Date: 2019-06-21 00:53:00.690222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ff7a6bf2ea0'
down_revision = '38d5e65972ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('measurements', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'measurements', 'users', ['user_id'], ['id'])
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_constraint('users_measurement_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'measurement_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('measurement_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_measurement_id_fkey', 'users', 'measurements', ['measurement_id'], ['id'])
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_constraint(None, 'measurements', type_='foreignkey')
    op.drop_column('measurements', 'user_id')
    # ### end Alembic commands ###
