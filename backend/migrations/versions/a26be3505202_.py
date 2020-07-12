"""empty message

Revision ID: a26be3505202
Revises: 399c0a0ee97b
Create Date: 2020-07-12 09:21:13.033566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26be3505202'
down_revision = '399c0a0ee97b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_results', sa.Column('test_id', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('test_results', sa.Column('user_id', sa.Integer(), nullable=False, server_default='0'))
    op.create_foreign_key(None, 'test_results', 'tests', ['test_id'], ['id'])
    op.create_foreign_key(None, 'test_results', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('doctor_id', sa.Integer(), nullable=False, server_default='0'))
    op.create_foreign_key(None, 'users', 'doctors', ['doctor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'doctor_id')
    op.drop_constraint(None, 'test_results', type_='foreignkey')
    op.drop_constraint(None, 'test_results', type_='foreignkey')
    op.drop_column('test_results', 'user_id')
    op.drop_column('test_results', 'test_id')
    # ### end Alembic commands ###