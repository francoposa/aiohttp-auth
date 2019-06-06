from app import usecases

stub_roles = [usecases.Role(id="0", role="family", permissions=["test"])]

stub_users = [
    usecases.User(
        username="domtoretto",
        pass_hash="$argon2i$v=19$m=102400,t=2,p=8$RYgxxriXMiZE6N17730vJQ$jK+rl+dt3EvZqX58d9k1GA",
        email="americanmuscle@fastnfurious.com",
        role_id="0",
    ),
    usecases.User(
        username="brian",
        pass_hash="$argon2i$v=19$m=102400,t=2,p=8$ijGmNKb03pszphQihPDe+w$JQKAk68EZcIVf7h+RUDMHA",
        email="importtuners@fastnfurious.com",
        role_id="0",
    ),
    usecases.User(
        username="roman",
        pass_hash="$argon2i$v=19$m=102400,t=2,p=8$BADg3Ptfq3WulZLyfq8V4g$HUmuNpGHBSWuVY6w3hI2RQ",
        email="ejectoseat@fastnfurious.com",
        role_id="0",
    ),
]


async def setup_db(role_pg_client, user_pg_client):

    for role in stub_roles:
        await role_pg_client.insert(role)

    for user in stub_users:
        await user_pg_client.insert(user)
