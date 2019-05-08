from typing import Optional, List

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import argon2

from app.infrastructure.datastore.postgres import UserPostgresClient, RolePostgresClient
from app.usecases import User, Role


class PostgresAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(
        self, user_client: UserPostgresClient, role_client: RolePostgresClient
    ):
        self.user_client = user_client
        self.role_client = role_client

    async def authorized_userid(self, identity: str) -> Optional[str]:
        users = await self.user_client.select_where(
            inclusion_map={"username": identity, "enabled": True}
        )
        if users:
            return identity

    async def permits(self, identity, permission, context=None) -> bool:
        if identity is None:
            return False
        users: List[User] = await self.user_client.select_where(
            inclusion_map={"username": identity}, exclusion_map={"enabled": False}
        )
        if users:
            user: User = users[0]
            roles: List[Role] = await self.role_client.select_where(
                inclusion_map={"role_id": user.role_id}
            )
            role: Role = roles[0]
            role_permissions: List[str] = role.permissions
            if permission in role_permissions:
                return True
        return False
