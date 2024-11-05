from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'XXXX_initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Example of a table creation, modify as necessary
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100)),
        sa.Column('email', sa.String(length=100)),
        sa.Column('phone', sa.String(length=15)),
        sa.Column('address', sa.String(length=255)),
        sa.Column('total_price', sa.Float),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('orders')
