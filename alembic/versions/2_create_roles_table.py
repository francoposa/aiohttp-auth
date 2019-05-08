"""create_roles_table

Revision ID: 23e1639bbbd6
Revises: 1
Create Date: 2019-05-02 15:26:25.396213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision = "2"
down_revision = "1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "roles",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("role", sa.String, nullable=False, unique=True),
        sa.Column("permissions", ARRAY(sa.String), nullable=False),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
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

    op.create_foreign_key(
        constraint_name="users_role_id_fkey",
        source_table="users",
        referent_table="roles",
        local_cols=["role_id"],
        remote_cols=["id"],
    )


def downgrade():
    op.drop_constraint("users_role_id_fkey", table_name="users", type_="foreignkey")
    op.drop_table("roles")
