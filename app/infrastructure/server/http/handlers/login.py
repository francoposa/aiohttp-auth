from aiohttp import web
from aiohttp_security import authorized_userid, remember

from app.infrastructure.app_constants import IDENTITY_POLICY, USER_CLIENT
from app.infrastructure.server.http.routes import PORTAL_NAME
from app.infrastructure.server.http.utils import redirect
from app.usecases import User

LOGIN_TEMPLATE = "login.html"


async def login(request):
    username = await authorized_userid(request)
    if username:
        return redirect(router=request.app.router, route_name=PORTAL_NAME)

    if request.method == "POST":
        form = await request.post()

        user_client = request.app[USER_CLIENT]
        authorized = await user_client.check_credentials(
            form["username"], form["password"]
        )

        if not authorized:
            return web.Response(text="Sorry, nerd")
        else:
            user: User = await user_client.select_first_where(
                include={"username": form["username"]}
            )
            identity_policy = request.app[IDENTITY_POLICY]
            await identity_policy.remember(
                request, response=None, identity=user.username
            )
            return redirect(router=request.app.router, route_name=PORTAL_NAME)

    template = request.app.jinja_env.get_template(LOGIN_TEMPLATE)
    return web.Response(text=await template.render_async({}), content_type="text/html")
