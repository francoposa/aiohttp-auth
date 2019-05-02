from app.usecases import Role
from app.infrastructure.datastore.postgres.clients.base import BasePostgresClient
from app.infrastructure.datastore.postgres.tables import ROLE


class RolePostgresClient(BasePostgresClient):
    def __init__(self, engine):
        super().__init__(Role, engine, ROLE)
