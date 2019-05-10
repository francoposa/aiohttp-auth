from passlib.hash import argon2

from app.infrastructure.datastore.postgres import UserPostgresClient


async def check_credentials(
    user_client: UserPostgresClient, username, password
) -> bool:
    users = await user_client.select_where(
        inclusion_map={"username": username, "enabled": True}
    )
    if users:
        user = users[0]
        return argon2.verify(password, user.pass_hash)
    return False
