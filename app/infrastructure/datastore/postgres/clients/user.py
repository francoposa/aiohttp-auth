from passlib.hash import argon2

from app.usecases import User
from app.infrastructure.datastore.postgres.clients.base import BasePostgresClient
from app.infrastructure.datastore.postgres.tables import USER


class UserPostgresClient(BasePostgresClient):
    def __init__(self, engine):
        super().__init__(User, engine, USER)

    async def check_credentials(self, username, password) -> bool:
        user: User = await self.select_first_where(
            inclusion_map={"username": username, "enabled": True}
        )
        if user:
            return argon2.verify(password, user.pass_hash)
        return False
