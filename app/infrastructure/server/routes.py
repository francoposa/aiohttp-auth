from aiohttp import web


HEALTH_PATH = "/api/v1/health"
HEALTH_NAME = "health"

LOGIN_PATH = "/login"
LOGIN_NAME = "login"
LOGIN_TEMPLATE = "login.html"

LOGOUT_PATH = "/logout"
LOGOUT_NAME = "logout"

PORTAL_PATH = "/portal"
PORTAL_NAME = "portal"
PORTAL_TEMPLATE = "portal.html"


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)
