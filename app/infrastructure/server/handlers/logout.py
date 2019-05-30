from app.infrastructure.server.routes import redirect, LOGIN_NAME
from app.infrastructure.server.session_utils import forget_session


async def logout(request):
    await forget_session(request)
    return redirect(router=request.app.router, route_name=LOGIN_NAME)
