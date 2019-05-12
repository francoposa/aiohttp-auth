"""
Setup functions for HTTP server.
"""
from typing import Awaitable

import aiohttp_cors
import jinja2
from aiohttp import web

from app.infrastructure.server.http.handlers import health, login

RUNNING_TASKS = "running_tasks"

HEALTH_PATH = "/api/v1/health"
HEALTH_NAME = "health"

INFO_PATH = "/api/v1/"
INFO_NAME = "info"

LOGIN_PATH = "/login"
LOGIN_NAME = "login"


def _setup_templates(app):
    jinja_loader = jinja2.PackageLoader("app.infrastructure", "templates")
    jinja_env = jinja2.Environment(
        loader=jinja_loader, auto_reload=False, enable_async=True
    )
    app.jinja_env = jinja_env


def _setup_routes(app):
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

    # Health check & Metadata
    app.router.add_get(HEALTH_PATH, health.health_check, name=HEALTH_NAME)
    app.router.add_get(INFO_PATH, health.info, name=INFO_NAME)

    app.router.add_get(LOGIN_PATH, login.login, name=LOGIN_NAME)
    app.router.add_post(LOGIN_PATH, login.login, name=LOGIN_NAME)


def configure_app(app: web.Application, startup_handler):
    """Configure the web.Application."""

    _setup_templates(app)
    _setup_routes(app)
    # Schedule custom startup routine.
    app.on_startup.append(startup_handler)


def register_dependency(app, constant_key, dependency, usecase=None):
    """Add dependencies used by the HTTP handlers."""

    if usecase is None:
        app[constant_key] = dependency
    else:
        if constant_key not in app:
            app[constant_key] = {}
        app[constant_key][usecase] = dependency


def register_task(app: web.Application, coro: Awaitable):
    """Register a background task with the aiohttp app.
    """

    if RUNNING_TASKS not in app:
        app[RUNNING_TASKS] = []

    task = app.loop.create_task(coro)
    app[RUNNING_TASKS].append(task)
