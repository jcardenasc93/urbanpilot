"""Create customer model

Revision ID: 264b86545c21
Revises: 
Create Date: 2021-09-17 01:01:58.339544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '264b86545c21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('middle_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('zipcode', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('customer')
    # ### end Alembic commands ###
