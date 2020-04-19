import argparse
import json
import os
from typing import Mapping

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiopg.sa import create_engine
from passlib.hash import argon2

from app.infrastructure.app_constants import USER_CLIENT
from app.infrastructure.datastore.postgres import UserPostgresClient

from app.infrastructure.server import setup_templates, setup_routes
from app.usecases import User


def on_startup(conf: Mapping):
    """Return a startup handler that will perform background tasks"""

    async def startup_handler(app: web.Application) -> None:
        """Run all initialization tasks.

        These are tasks that should be run after the event loop has been started but before the HTTP
        server has been started.
        """
        setup_templates(app)
        setup_routes(app)
        # Registers session middleware
        setup_session(
            app,
            EncryptedCookieStorage(
                secret_key=b"Thirty  two  length  bytes  key.", max_age=60 * 5
            ),
        )

        # Instantiate database clients
        pg_engine = await create_engine(**conf["postgres"])
        user_pg_client = UserPostgresClient(pg_engine)

        # await user_pg_client.insert(User(username="test", email="test@example.com", pass_hash = argon2.hash("test"), role_id=""))

        # Register database clients
        app[USER_CLIENT] = user_pg_client

        async def cleanup(app):
            """Perform required cleanup on shutdown"""
            pg_engine.close()
            await pg_engine.wait_closed()

        app.on_shutdown.append(cleanup)

    return startup_handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file")
    args = parser.parse_args()

    # Load config.
    with open(args.config, "r") as conf_file:
        conf = json.load(conf_file)

    app = web.Application()
    app.on_startup.append(on_startup(conf))
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)
