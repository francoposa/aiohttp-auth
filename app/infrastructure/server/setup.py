"""
Setup functions for HTTP server.
"""

import aiohttp_cors
import jinja2
from aiohttp import web

from app.infrastructure.app_constants import TEMPLATE_ENGINE
from app.infrastructure.server.handlers import portal, logout
from app.infrastructure.server.handlers import login, health
from app.infrastructure.server.routes import (
    HEALTH_NAME,
    HEALTH_PATH,
    LOGIN_NAME,
    LOGIN_PATH,
    PORTAL_NAME,
    PORTAL_PATH,
    LOGOUT_PATH,
    LOGOUT_NAME,
)


def setup_templates(app):
    jinja_loader = jinja2.PackageLoader("app.infrastructure.server", "templates")
    jinja_env = jinja2.Environment(
        loader=jinja_loader, auto_reload=False, enable_async=True
    )
    app[TEMPLATE_ENGINE] = jinja_env


def setup_routes(app):
    """Add routes to the given aiohttp app."""

    # Default cors settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    # Health check
    app.router.add_get(HEALTH_PATH, health.health_check, name=HEALTH_NAME)

    # Login
    app.router.add_get(LOGIN_PATH, login.login, name=LOGIN_NAME)
    app.router.add_post(LOGIN_PATH, login.login, name=LOGIN_NAME)

    # Portal
    app.router.add_get(PORTAL_PATH, portal.portal, name=PORTAL_NAME)

    # Logout
    app.router.add_get(LOGOUT_PATH, logout.logout, name=LOGOUT_NAME)
