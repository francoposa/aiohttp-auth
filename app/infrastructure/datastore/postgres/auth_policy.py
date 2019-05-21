from typing import Optional, List

from aiohttp_security.abc import AbstractAuthorizationPolicy

from app.infrastructure.datastore.postgres import UserPostgresClient, RolePostgresClient
from app.usecases import User, Role


class PostgresAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(
        self, user_client: UserPostgresClient, role_client: RolePostgresClient
    ):
        self.user_client = user_client
        self.role_client = role_client

    async def authorized_userid(self, identity: str) -> Optional[str]:
        user: User = await self.user_client.select_where(
            inclusion_map={"username": identity, "enabled": True}
        )
        if user:
            return identity

    async def permits(self, identity, permission, context=None) -> bool:
        if identity is None:
            return False
        user: User = await self.user_client.select_first_where(
            inclusion_map={"username": identity, "enabled": True}
        )
        if user:
            role: Role = await self.role_client.select_first_where(
                inclusion_map={"role_id": user.role_id}
            )
            role_permissions: List[str] = role.permissions
            if permission in role_permissions:
                return True
        return False
