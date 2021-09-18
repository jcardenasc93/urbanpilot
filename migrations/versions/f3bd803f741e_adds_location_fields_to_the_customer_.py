"""Adds location fields to the customer model

Revision ID: f3bd803f741e
Revises: 264b86545c21
Create Date: 2021-09-18 14:06:40.562842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3bd803f741e"
down_revision = "264b86545c21"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("customer", sa.Column("city", sa.String(length=20), nullable=True))
    op.add_column("customer", sa.Column("county", sa.String(length=20), nullable=True))
    op.add_column("customer", sa.Column("state", sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("customer", "zipcode", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "customer", "email", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "customer", "last_name", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.alter_column(
        "customer", "first_name", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.drop_column("customer", "state")
    op.drop_column("customer", "county")
    op.drop_column("customer", "city")
    # ### end Alembic commands ###
