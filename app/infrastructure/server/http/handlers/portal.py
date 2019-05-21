from aiohttp import web
from aiohttp_security import authorized_userid, remember, AbstractIdentityPolicy
from aiohttp_security.api import IDENTITY_KEY

from app.infrastructure.app_constants import IDENTITY_POLICY, USER_CLIENT
from app.infrastructure.server.http.routes import LOGIN_NAME
from app.infrastructure.server.http.utils import redirect

PORTAL_TEMPLATE = "portal.html"


async def portal(request):
    identity_policy: AbstractIdentityPolicy = request.app[IDENTITY_POLICY]
    username: str = await identity_policy.identify(request)
    if username:
        user_client = request.app[USER_CLIENT]
        user = await user_client.select_first_where(
            inclusion_map={"username": username}
        )
        template = request.app.jinja_env.get_template(PORTAL_TEMPLATE)
        return web.Response(
            text=await template.render_async({"user": user}), content_type="text/html"
        )
    return redirect(router=request.app.router, route_name=LOGIN_NAME)
