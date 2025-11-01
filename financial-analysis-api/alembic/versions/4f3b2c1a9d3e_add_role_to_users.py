"""add role column to users

Revision ID: 4f3b2c1a9d3e
Revises: 
Create Date: 2025-10-25 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f3b2c1a9d3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add role column with default 'user'
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=False, server_default=sa.text("'user'")))


def downgrade():
    op.drop_column('users', 'role')
