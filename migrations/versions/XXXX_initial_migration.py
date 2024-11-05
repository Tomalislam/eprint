from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'XXXX_initial_migration'  # replace XXXX with a unique identifier
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create the orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )

    # Create the order_files table to hold details about the files associated with each order
    op.create_table(
        'order_files',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('total_pages', sa.Integer(), nullable=False),
        sa.Column('page_size', sa.String(length=10), nullable=False),
        sa.Column('color_type', sa.String(length=20), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE')
    )

def downgrade():
    # Drop the order_files table first to maintain referential integrity
    op.drop_table('order_files')
    op.drop_table('orders')
