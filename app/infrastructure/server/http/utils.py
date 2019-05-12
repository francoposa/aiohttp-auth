from aiohttp import web


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)
