"""
HTTP health check.
"""

import json
import os
import socket

from aiohttp import web

from app.infrastructure.datastore.postgres.auth.utils import check_credentials

ENV_INFO_KEYS = [
    "BUILD_DATE",
    "BUILD_URL",
    "GIT_COMMIT",
    "GIT_COMMIT_DATE",
    "IMAGE_NAME",
    "SERVER_HOSTNAME",
    "SERVICE_ID",
    "SERVICE_NAME",
]
INFO = {key.lower(): os.environ.get(key) for key in ENV_INFO_KEYS}
INFO["hostname"] = socket.gethostname()


def _dumps(obj):
    """Pretty JSON"""
    return json.dumps(obj, indent=4, sort_keys=True) + "\n"


async def health_check(request):
    """Health check handler."""
    return web.json_response({"status": "OK"})


async def info(request):
    """Metadata."""
    if await check_credentials(
        user_client=request.app.user_client, username="test", password="testy"
    ):
        return web.json_response(INFO, dumps=_dumps)
    return web.HTTPUnauthorized(body=b"Invalid username/password combination")
