from aiohttp import web
from aiohttp_security import authorized_userid, remember
from aiohttp_security.api import IDENTITY_KEY

from app.infrastructure.server.http.utils import redirect

PORTAL_TEMPLATE = "portal.html"


async def portal(request):
    identity_policy = request.app[IDENTITY_KEY]
    user = await identity_policy.identify(request)
    if user:
        template = request.app.jinja_env.get_template(PORTAL_TEMPLATE)
        return web.Response(
            text=await template.render_async({"user": user}), content_type="text/html"
        )
    if request.method == "POST":
        form = await request.post()

        authorized = await request.app.user_client.check_credentials(
            form["username"], form["password"]
        )

        if not authorized:
            return web.Response(text="Sorry, nerd")
        else:
            response = web.Response(text="Welcome, let's get this money")

            users = await request.app.user_client.select_where(
                inclusion_map={"username": form["username"]}
            )
            user = users[0]
            await remember(request, response, user.username)
            return response

    template = request.app.jinja_env.get_template(LOGIN_TEMPLATE)
    return web.Response(text=await template.render_async({}), content_type="text/html")
