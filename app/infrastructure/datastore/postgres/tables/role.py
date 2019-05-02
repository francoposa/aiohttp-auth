import sqlalchemy as sa

from app.infrastructure.datastore.postgres.tables.metadata import METADATA


ROLE = sa.Table(
    "roles",
    METADATA,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("role", sa.String, nullable=False),
    sa.Column("permission", sa.String, nullable=False),
    sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column(
        "updated_at",
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    ),
)
