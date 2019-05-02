"""create_users_table

Revision ID: 1
Revises: 
Create Date: 2019-05-02 19:48:41.668529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("pass", sa.String, nullable=False),
        sa.Column("email", sa.String),
        sa.Column("role", sa.String),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
        ),
    )


def downgrade():
    op.drop_table("users")
