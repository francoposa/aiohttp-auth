from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import argon2

from app.infrastructure.datastore.postgres import UserPostgresClient, RolePostgresClient


class PostgresAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(
        self, user_client: UserPostgresClient, role_client: RolePostgresClient
    ):
        self.user_client = user_client
        self.role_client = role_client
