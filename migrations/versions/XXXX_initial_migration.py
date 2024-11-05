"""initial migration

Revision ID: abc123456789
Revises: 
Create Date: 2024-11-05 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = 'abc123456789'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table called 'orders'
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    # Drop the 'orders' table
    op.drop_table('orders')
