from aiohttp import web
from aiohttp_security import authorized_userid, remember

from app.infrastructure.datastore.postgres.auth.utils import check_credentials
from app.infrastructure.server.http.utils import redirect

LOGIN_TEMPLATE = "login.html"


async def login(request):
    username = await authorized_userid(request)
    if username:
        return web.Response(text="You're already logged in, let's get this money")

    if request.method == "POST":
        form = await request.post()

        authorized = await check_credentials(
            request.app.user_client, form["username"], form["password"]
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
