from typing import Optional

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import argon2

from app.infrastructure.datastore.postgres import UserPostgresClient, RolePostgresClient


class PostgresAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(
        self, user_client: UserPostgresClient, role_client: RolePostgresClient
    ):
        self.user_client = user_client
        self.role_client = role_client

    async def authorized_userid(self, identity: str) -> Optional[str]:
        users = await self.user_client.select_where(
            inclusion_map={"username": identity}, exclusion_map={"enabled": False}
        )
        if users:
            return identity

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False