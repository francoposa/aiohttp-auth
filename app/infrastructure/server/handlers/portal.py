from aiohttp import web


from app.infrastructure.app_constants import USER_CLIENT, TEMPLATE_ENGINE
from app.infrastructure.server.routes import LOGIN_NAME, PORTAL_TEMPLATE
from app.infrastructure.server.routes import redirect
from app.infrastructure.server.session_utils import identify_session


async def portal(request):
    username: str = await identify_session(request)
    if username:
        user_client = request.app[USER_CLIENT]
        user = await user_client.select_first_where(include={"username": username})
        template = request.app[TEMPLATE_ENGINE].get_template(PORTAL_TEMPLATE)
        return web.Response(
            text=await template.render_async({"user": user}), content_type="text/html"
        )
    return redirect(router=request.app.router, route_name=LOGIN_NAME)
