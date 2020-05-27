from aiohttp import web

from app.infrastructure.app_constants import USER_CLIENT, TEMPLATE_ENGINE
from app.infrastructure.server.routes import LOGIN_TEMPLATE, PORTAL_NAME
from app.infrastructure.server.routes import redirect
from app.infrastructure.server.session_utils import register_session, identify_session
from app.usecases import User


async def login(request):
    username = await identify_session(request)
    if username:
        return redirect(router=request.app.router, route_name=PORTAL_NAME)

    template_data = {}
    if request.method == "POST":
        form = await request.post()
        user_client = request.app[USER_CLIENT]
        authorized = await user_client.check_credentials(
            form["username"], form["password"]
        )
        if authorized:
            user: User = await user_client.select_first_where(
                include={"username": form["username"]}
            )
            await register_session(request, identity=user.username)
            return redirect(router=request.app.router, route_name=PORTAL_NAME)
        else:
            template_data["error"] = "Username or password is incorrect"

    template = request.app[TEMPLATE_ENGINE].get_template(LOGIN_TEMPLATE)
    return web.Response(
        text=await template.render_async(template_data), content_type="text/html"
    )
