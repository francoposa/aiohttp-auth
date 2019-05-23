import argparse
import json
import os
from typing import Mapping

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiopg.sa import create_engine

from app.infrastructure.datastore.postgres import UserPostgresClient, RolePostgresClient
from app.infrastructure.datastore.postgres.auth_policy import (
    PostgresAuthorizationPolicy,
)
from app.infrastructure import app_constants
from app.infrastructure.server import http


def on_startup(conf: Mapping):
    """Return a startup handler that will perform background tasks"""

    async def startup_handler(app: web.Application) -> None:
        """Run all initialization tasks.

        These are tasks that should be run after the event loop has been started but before the HTTP
        server has been started.
        """

        # Instantiate database clients
        pg_engine = await create_engine(**conf["postgres"])
        user_pg_client = UserPostgresClient(pg_engine)
        role_pg_client = RolePostgresClient(pg_engine)
        # Register database clients
        app[app_constants.USER_CLIENT] = user_pg_client

        # Registers session middleware
        setup_session(
            app,
            EncryptedCookieStorage(
                secret_key=b"Thirty  two  length  bytes  key.", max_age=60 * 5
            ),
        )

        # Instantiate and Register aiohttp_security policies
        setup_security(
            app,
            SessionIdentityPolicy(),
            PostgresAuthorizationPolicy(
                user_client=user_pg_client, role_client=role_pg_client
            ),
        )

    return startup_handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file")
    args = parser.parse_args()

    # Load config.
    with open(args.config, "r") as conf_file:
        conf = json.load(conf_file)

    app = web.Application()
    http.configure_app(app, on_startup(conf))
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
